import threading
import queue
import sys
import os
from brain.groq_chat import AtlasBrain
from voice.listener import Listener
from voice.stt import SpeechToText
from voice.speaker import Speaker
from voice.wake_word import WakeWord


class InputHandler:
    """Handles both keyboard and voice input concurrently."""

    def __init__(self):
        self.atlas = AtlasBrain()
        self.speaker = Speaker()
        self.listener = Listener(silence_threshold=500, silence_timeout=2.0)  # Increased timeout
        self.stt = SpeechToText()
        self.wake = WakeWord()
        
        # Intent detection and execution
        from brain.intent_detector import IntentDetector
        from brain.executor import CommandExecutor
        self.intent_detector = IntentDetector()
        self.executor = CommandExecutor()
        
        # Shared input queue for both voice and keyboard
        self.input_queue = queue.Queue()
        
        # Control flags
        self.running = True
        self.conversation_mode = False
        self.wake_word_active = True
        self.last_interaction_time = None
        self.conversation_timeout = 30  # seconds of inactivity before exiting conversation
        
        # Confirmation system
        self.pending_confirmation = None  # Store pending action: {'intent': 'delete_file', 'params': {...}}
        
        # Lock for console output
        self.output_lock = threading.Lock()

    def print_header(self):
        """Print the professional ATLAS header."""
        with self.output_lock:
            print("\n" + "=" * 50)
            print(" " * 17 + "A T L A S")
            print("=" * 50)
            print()
            print("Status      : 🟢 Listening")
            print("Wake Word   : Enabled")
            print("Memory      : Connected")
            print("AI          : Groq")
            print()
            print("-" * 50)
            print()

    def print_prompt(self):
        """Print the user input prompt."""
        with self.output_lock:
            print("\nYou : ", end='', flush=True)

    def print_response(self, text):
        """Print ATLAS response."""
        with self.output_lock:
            print(f"\n\nATLAS : {text}")

    def process_user_input(self, text):
        """
        Unified input processor for both voice and keyboard.
        This is the central function that handles all user input.
        """
        if not text or not text.strip():
            return
        
        text = text.strip()
        text_lower = text.lower()
        
        # Check for exit commands
        if text_lower in ["exit", "quit", "stop", "goodbye"]:
            self.print_response("Goodbye, Sir.")
            self.speaker.speak("Goodbye, Sir.")
            self.running = False
            return
        
        # FIRST: Check if there's a pending confirmation
        if self.pending_confirmation is not None:
            # Confirmation words
            if text_lower in ["yes", "y", "yeah", "yep", "confirm", "proceed", "do it", "go ahead", "okay", "ok"]:
                # User confirmed - execute the pending action
                pending = self.pending_confirmation
                self.pending_confirmation = None  # Clear immediately
                
                try:
                    with self.output_lock:
                        print(f"\n[Executing: {pending['intent']}...]", flush=True)
                    
                    success, message = self.executor.execute(pending['intent'], pending['params'])
                    self.print_response(message)
                    self.speaker.speak(message)
                    return
                except Exception as e:
                    error_msg = f"Error executing command: {str(e)}, Sir."
                    self.print_response(error_msg)
                    self.speaker.speak(error_msg)
                    return
            
            # Cancellation words
            elif text_lower in ["no", "n", "cancel", "abort", "stop", "never mind", "nevermind"]:
                # User cancelled
                self.pending_confirmation = None
                cancel_msg = "Action cancelled, Sir."
                self.print_response(cancel_msg)
                self.speaker.speak(cancel_msg)
                return
            
            else:
                # Not a clear yes/no - ask again
                clarify_msg = "Please say 'yes' to confirm or 'no' to cancel, Sir."
                self.print_response(clarify_msg)
                self.speaker.speak(clarify_msg)
                return
        
        # NO pending confirmation - proceed with normal intent detection
        try:
            # Detect intent
            intent, params = self.intent_detector.detect_intent(text)
            
            if intent == 'chat':
                # Regular conversation - send to Groq
                reply = self.atlas.chat(text)
                self.print_response(reply)
                self.speaker.speak(reply)
            else:
                # Command detected - execute it
                with self.output_lock:
                    print(f"\n[Executing: {intent}...]", flush=True)
                
                result = self.executor.execute(intent, params)
                
                # Check if result is a tuple with 3 elements (confirmation needed)
                if isinstance(result, tuple) and len(result) == 3 and result[2] == 'needs_confirmation':
                    # Store pending confirmation
                    self.pending_confirmation = {
                        'intent': intent,
                        'params': {**params, 'confirmed': True}  # Add confirmed flag
                    }
                    # Show confirmation message
                    _, message, _ = result
                    self.print_response(message)
                    self.speaker.speak(message)
                else:
                    # Normal execution result
                    success, message = result
                    if success:
                        self.print_response(message)
                        self.speaker.speak(message)
                    else:
                        # Execution failed, provide error message
                        self.print_response(message)
                        self.speaker.speak(message)
                    
        except Exception as e:
            error_msg = "I encountered an error processing that request, Sir."
            self.print_response(error_msg)
            self.speaker.speak(error_msg)
            print(f"Error: {e}")

    def voice_input_thread(self):
        """Background thread for voice input."""
        import time
        
        while self.running:
            try:
                # Wait for wake word if not in conversation mode
                if self.wake_word_active and not self.conversation_mode:
                    self.wake.wait(silent=True)
                    if not self.running:
                        break
                    
                    self.conversation_mode = True
                    self.last_interaction_time = time.time()
                    wake_msg = "Yes, Sir."
                    
                    with self.output_lock:
                        print(f"\n\nATLAS : {wake_msg}")
                    
                    self.speaker.speak(wake_msg)
                    self.print_prompt()
                
                # Check conversation timeout
                if self.conversation_mode and self.last_interaction_time:
                    if time.time() - self.last_interaction_time > self.conversation_timeout:
                        self.conversation_mode = False
                        with self.output_lock:
                            print("\n\n[Conversation timeout - Waiting for wake word...]")
                        self.print_prompt()
                        continue
                
                # Listen for voice input (longer timeout, silent mode)
                audio_file = self.listener.listen(timeout=15, silent=True)
                
                if audio_file is None:
                    # No speech detected, stay in conversation mode
                    continue
                
                # Transcribe the audio
                text = self.stt.transcribe(audio_file)
                
                # Validate transcription - ignore empty or very short noise
                if not text or len(text.strip()) < 3:
                    continue
                
                # Update last interaction time
                self.last_interaction_time = time.time()
                
                # Display what was heard
                with self.output_lock:
                    print(text)
                
                # Add to input queue
                self.input_queue.put(("voice", text))
                
            except Exception as e:
                if self.running:
                    print(f"\nVoice input error: {e}")
                    self.print_prompt()

    def keyboard_input_thread(self):
        """Background thread for keyboard input."""
        import time
        
        while self.running:
            try:
                # Read keyboard input
                text = input()
                
                if text.strip():
                    # Keyboard input activates conversation mode
                    if not self.conversation_mode:
                        self.conversation_mode = True
                    
                    # Update last interaction time
                    self.last_interaction_time = time.time()
                    
                    # Add to input queue
                    self.input_queue.put(("keyboard", text.strip()))
                else:
                    # Empty input, just reprint prompt
                    self.print_prompt()
                    
            except EOFError:
                # Handle Ctrl+D or end of input
                break
            except Exception as e:
                if self.running:
                    print(f"\nKeyboard input error: {e}")
                    self.print_prompt()

    def main_processing_loop(self):
        """Main thread that processes inputs from the queue."""
        while self.running:
            try:
                # Get next input from queue (with timeout to check running flag)
                try:
                    source, text = self.input_queue.get(timeout=0.5)
                except queue.Empty:
                    continue
                
                # Process the input through unified pipeline
                self.process_user_input(text)
                
                # Print prompt for next input
                if self.running:
                    self.print_prompt()
                    
            except Exception as e:
                if self.running:
                    print(f"\nProcessing error: {e}")
                    self.print_prompt()

    def run(self):
        """Start ATLAS with concurrent voice and keyboard input."""
        try:
            # Print header
            self.print_header()
            print("Say 'Hey Jarvis' to activate voice mode.")
            print("Or type your command directly below.\n")
            self.print_prompt()
            
            # Start voice input thread
            voice_thread = threading.Thread(target=self.voice_input_thread, daemon=True)
            voice_thread.start()
            
            # Start keyboard input thread
            keyboard_thread = threading.Thread(target=self.keyboard_input_thread, daemon=True)
            keyboard_thread.start()
            
            # Run main processing loop in current thread
            self.main_processing_loop()
            
        except KeyboardInterrupt:
            print("\n\nShutting down...")
        finally:
            # Clean shutdown
            self.running = False
            self.wake.close()
            print("\nATLAS offline.")


def main():
    """Entry point for ATLAS."""
    handler = InputHandler()
    handler.run()


if __name__ == "__main__":
    main()
