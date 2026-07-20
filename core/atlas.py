"""
Atlas Orchestration Module
Main orchestrator that coordinates all subsystems.
"""

import queue
import threading
from typing import Optional

from brain.groq_chat import AtlasBrain
from brain.intent_detector import IntentDetector
from brain.executor import CommandExecutor
from voice.listener import Listener
from voice.stt import SpeechToText
from voice.speaker import Speaker
from voice.wake_word import WakeWord
from ui.console import Console
from ui.input_handler import InputThreadManager
from core.conversation import ConversationState
from core.confirmation import ConfirmationManager


class Atlas:
    """Main orchestrator for the ATLAS AI assistant."""
    
    def __init__(self):
        """Initialize Atlas and all subsystems."""
        # UI subsystem
        self.console = Console()
        
        # Brain subsystem
        self.brain = AtlasBrain()
        self.intent_detector = IntentDetector()
        self.executor = CommandExecutor()
        
        # Voice subsystem
        self.speaker = Speaker()
        self.listener = Listener(silence_threshold=500, silence_timeout=2.0)
        self.stt = SpeechToText()
        self.wake = WakeWord()
        
        # State management
        self.conversation_state = ConversationState(timeout=30)
        self.confirmation_manager = ConfirmationManager()
        
        # Input queue and control flags
        self.input_queue = queue.Queue()
        self.running = True
        
        # Input thread manager
        voice_system = {
            'wake': self.wake,
            'listener': self.listener,
            'stt': self.stt,
            'speaker': self.speaker
        }
        self.input_manager = InputThreadManager(
            self.input_queue,
            self.console,
            voice_system,
            self.conversation_state
        )
    
    def process_user_input(self, text: str):
        """
        Process user input through the intelligence pipeline.
        
        Args:
            text: User input text
        """
        if not text or not text.strip():
            return
        
        text = text.strip()
        text_lower = text.lower()
        
        # Check for exit commands
        if text_lower in ["exit", "quit", "stop", "goodbye"]:
            self.console.print_response("Goodbye, Sir.")
            self.speaker.speak("Goodbye, Sir.")
            self.running = False
            return
        
        # Handle pending confirmation
        if self.confirmation_manager.has_pending():
            response = self.confirmation_manager.process_response(text)
            
            if response == 'confirmed':
                # Execute the pending action
                pending = self.confirmation_manager.get_pending()
                self.confirmation_manager.clear_pending()
                
                try:
                    self.console.print_message(f"\n[Executing: {pending['intent']}...]")
                    success, message = self.executor.execute(pending['intent'], pending['params'])
                    self.console.print_response(message)
                    self.speaker.speak(message)
                except Exception as e:
                    error_msg = f"Error executing command: {str(e)}, Sir."
                    self.console.print_response(error_msg)
                    self.speaker.speak(error_msg)
                return
            
            elif response == 'cancelled':
                # User cancelled
                self.confirmation_manager.clear_pending()
                cancel_msg = "Action cancelled, Sir."
                self.console.print_response(cancel_msg)
                self.speaker.speak(cancel_msg)
                return
            
            else:
                # Unclear response
                clarify_msg = "Please say 'yes' to confirm or 'no' to cancel, Sir."
                self.console.print_response(clarify_msg)
                self.speaker.speak(clarify_msg)
                return
        
        # No pending confirmation - detect intent
        try:
            intent, params = self.intent_detector.detect_intent(text)
            
            if intent == 'chat':
                # Regular conversation
                reply = self.brain.chat(text)
                self.console.print_response(reply)
                self.speaker.speak(reply)
            else:
                # Command detected - execute it
                self.console.print_message(f"\n[Executing: {intent}...]")
                result = self.executor.execute(intent, params)
                
                # Check if confirmation is needed
                if isinstance(result, tuple) and len(result) == 3 and result[2] == 'needs_confirmation':
                    # Store pending confirmation
                    self.confirmation_manager.set_pending(intent, params)
                    _, message, _ = result
                    self.console.print_response(message)
                    self.speaker.speak(message)
                else:
                    # Normal execution result
                    success, message = result
                    self.console.print_response(message)
                    self.speaker.speak(message)
                    
        except Exception as e:
            error_msg = "I encountered an error processing that request, Sir."
            self.console.print_response(error_msg)
            self.speaker.speak(error_msg)
            print(f"Error: {e}")
    
    def main_processing_loop(self):
        """Main thread that processes inputs from the queue."""
        while self.running:
            try:
                # Get next input from queue
                try:
                    source, text, recognition_id = self.input_queue.get(timeout=0.5)
                except queue.Empty:
                    continue
                
                # Log processing start
                print(f"[{recognition_id}] 🔄 Processing started...")
                
                # Process the input
                self.process_user_input(text)
                
                # Log processing complete
                print(f"[{recognition_id}] ✓ Processing complete")
                
                # Print prompt for next input
                if self.running:
                    self.console.print_prompt()
                    
            except Exception as e:
                if self.running:
                    print(f"\nProcessing error: {e}")
                    self.console.print_prompt()
    
    def run(self):
        """Start ATLAS and run the main loop."""
        try:
            # Print header
            self.console.print_header()
            print("Say 'Hey Jarvis' to activate voice mode.")
            print("Or type your command directly below.\n")
            self.console.print_prompt()
            
            # Start input threads
            self.input_manager.start_threads()
            
            # Run main processing loop in current thread
            self.main_processing_loop()
            
        except KeyboardInterrupt:
            print("\n\nShutting down...")
        finally:
            # Clean shutdown
            self.running = False
            self.input_manager.stop()
            self.wake.close()
            print("\nATLAS offline.")
