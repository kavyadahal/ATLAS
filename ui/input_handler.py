"""
Input Handler Module
Manages keyboard and voice input threads.
"""

import threading
import queue
import time
from typing import Callable, Optional


class InputThreadManager:
    """Manages concurrent keyboard and voice input threads."""
    
    def __init__(
        self,
        input_queue: queue.Queue,
        console,
        voice_system,
        conversation_state
    ):
        """
        Initialize input thread manager.
        
        Args:
            input_queue: Queue to place input into
            console: Console instance for output
            voice_system: Dictionary with voice components (wake, listener, stt, speaker)
            conversation_state: ConversationState instance
        """
        self.input_queue = input_queue
        self.console = console
        self.voice_system = voice_system
        self.conversation_state = conversation_state
        self.running = True
    
    def voice_input_thread(self):
        """Background thread for voice input."""
        from voice.speaking_state import get_speaking_state
        
        wake = self.voice_system['wake']
        listener = self.voice_system['listener']
        stt = self.voice_system['stt']
        speaker = self.voice_system['speaker']
        
        while self.running:
            try:
                # Wait for wake word if not in conversation mode
                if not self.conversation_state.is_active():
                    wake.wait(silent=True)
                    if not self.running:
                        break
                    
                    self.conversation_state.activate()
                    wake_msg = "Yes, Sir."
                    
                    self.console.print_response(wake_msg)
                    speaker.speak(wake_msg)
                    self.console.print_prompt()
                
                # Check conversation timeout
                if self.conversation_state.check_timeout():
                    self.console.print_message("\n\n[Conversation timeout - Waiting for wake word...]")
                    self.console.print_prompt()
                    continue
                
                # Listen for voice input (longer timeout, silent mode)
                audio_file, recognition_id = listener.listen(timeout=15, silent=True)
                
                # If no speech detected, audio_file will be None
                if audio_file is None:
                    if recognition_id:
                        print(f"[{recognition_id}] No speech - continuing to listen")
                    continue
                
                # Transcribe the audio with recognition ID
                text = stt.transcribe(audio_file, recognition_id)
                
                # Validate transcription - ignore empty or very short noise
                if not text or len(text.strip()) < 3:
                    print(f"[{recognition_id}] ❌ Transcript too short or empty - ignored")
                    continue
                
                # Echo protection - check if this is assistant's own speech
                speaking_state = get_speaking_state()
                if speaking_state.is_echo(text):
                    print(f"[{recognition_id}] ❌ Echo detected - ignored")
                    continue
                
                # Update last interaction time
                self.conversation_state.update_interaction()
                
                # Display what was heard
                self.console.print_message(f"[{recognition_id}] ✅ USER INPUT: '{text}'")
                
                # Add to input queue with recognition ID
                print(f"[{recognition_id}] 📤 Queued for processing")
                self.input_queue.put(("voice", text, recognition_id))
                
            except Exception as e:
                if self.running:
                    print(f"\nVoice input error: {e}")
                    import traceback
                    traceback.print_exc()
                    self.console.print_prompt()
    
    def keyboard_input_thread(self):
        """Background thread for keyboard input."""
        while self.running:
            try:
                # Read keyboard input
                text = input()
                
                if text.strip():
                    # Keyboard input activates conversation mode
                    if not self.conversation_state.is_active():
                        self.conversation_state.activate()
                    
                    # Update last interaction time
                    self.conversation_state.update_interaction()
                    
                    # Add to input queue with recognition ID
                    recognition_id = f"KBD_{int(time.time() * 1000)}"
                    self.input_queue.put(("keyboard", text.strip(), recognition_id))
                else:
                    # Empty input, just reprint prompt
                    self.console.print_prompt()
                    
            except EOFError:
                # Handle Ctrl+D or end of input
                break
            except Exception as e:
                if self.running:
                    print(f"\nKeyboard input error: {e}")
                    self.console.print_prompt()
    
    def start_threads(self):
        """Start both input threads."""
        voice_thread = threading.Thread(target=self.voice_input_thread, daemon=True)
        keyboard_thread = threading.Thread(target=self.keyboard_input_thread, daemon=True)
        
        voice_thread.start()
        keyboard_thread.start()
        
        return voice_thread, keyboard_thread
    
    def stop(self):
        """Stop all input threads."""
        self.running = False
