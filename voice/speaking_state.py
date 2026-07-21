"""
Central speaking state manager for full-duplex protection.
Prevents the assistant from listening to its own speech.
"""

import threading
import time
from difflib import SequenceMatcher
from collections import deque


class SpeakingState:
    """
    Thread-safe speaking state manager.
    Coordinates between TTS output and speech recognition to prevent echo.
    """
    
    def __init__(self):
        self._lock = threading.RLock()
        self._is_speaking = False
        self._last_spoken_text = ""
        self._speaking_finished_time = 0
        self.resume_delay = 0.8  # 800ms delay after speech ends (PART 1: Post-TTS cooldown)
        
        # Event-based synchronization: Listener threads wait on this event
        # Set when safe to listen, cleared when speaking starts
        self._can_listen_event = threading.Event()
        self._can_listen_event.set()  # Initially can listen
        
        # PART 1: Duplicate transcript suppression
        self._recent_transcripts = deque(maxlen=5)  # Store last 5 transcripts
        self._transcript_times = deque(maxlen=5)
        self.duplicate_window = 2.0  # seconds
        
        # PART 1: Short utterance filtering
        self._short_phrases = {
            'thanks', 'thank you', 'okay', 'ok', 'hmm', 'uh', 'yes', 'no',
            'yeah', 'yep', 'nope', 'sure', 'right', 'good', 'fine', 'well'
        }
    
    def start_speaking(self, text: str = ""):
        """Mark that TTS has started. Call BEFORE audio generation."""
        with self._lock:
            self._is_speaking = True
            self._last_spoken_text = self._normalize(text)
            # Clear the event to block any listener threads
            self._can_listen_event.clear()
            print("[TTS] Speaking...")
    
    def stop_speaking(self):
        """
        Mark that TTS has finished. Call AFTER audio playback completes.
        This method will block for the resume_delay period, then signal listeners.
        """
        with self._lock:
            self._is_speaking = False
            self._speaking_finished_time = time.time()
            print("[TTS] Finished")
            print(f"[Listener] Cooldown {int(self.resume_delay * 1000)}ms...")
        
        # CRITICAL: Wait for cooldown BEFORE setting the event
        # This ensures no listener can proceed until the delay has elapsed
        time.sleep(self.resume_delay)
        
        with self._lock:
            # Now it's safe - signal all waiting listener threads
            self._can_listen_event.set()
            print("[Listener] Ready to resume")
    
    def is_speaking(self) -> bool:
        """Check if assistant is currently speaking."""
        with self._lock:
            return self._is_speaking
    
    def can_listen(self) -> bool:
        """
        Check if it's safe to accept microphone input.
        Returns False if:
        - Currently speaking
        - Within resume_delay period after speaking finished
        """
        with self._lock:
            if self._is_speaking:
                return False
            
            # Check if we're still in the resume delay period (PART 1: Cooldown)
            if self._speaking_finished_time > 0:
                elapsed = time.time() - self._speaking_finished_time
                if elapsed < self.resume_delay:
                    return False
            
            return True
    
    def wait_until_can_listen(self, timeout: float = None):
        """
        Block until it's safe to listen using event-based synchronization.
        Used by listener to wait for TTS to finish.
        
        Args:
            timeout: Maximum time to wait in seconds (None = wait forever)
        
        Returns:
            True if can listen, False if timeout occurred
        """
        # Wait on the event instead of polling
        result = self._can_listen_event.wait(timeout=timeout)
        
        if result:
            print("[Listener] Resumed")
        else:
            print("[Listener] Wait timeout!")
        
        return result
    
    def is_echo(self, recognized_text: str, similarity_threshold: float = 0.75) -> bool:
        """
        Check if recognized text is likely an echo of assistant's own speech.
        Uses fuzzy matching with normalized strings.
        
        Args:
            recognized_text: Text from speech recognizer
            similarity_threshold: Minimum similarity (0-1) to consider echo
        
        Returns:
            True if text is likely an echo, False otherwise
        """
        if not recognized_text:
            return False
        
        with self._lock:
            normalized_input = self._normalize(recognized_text)
            
            # PART 1: Check for duplicate transcripts
            if self._is_duplicate(normalized_input):
                print(f"[Recognition Ignored: duplicate] '{recognized_text}'")
                return True
            
            # PART 1: Check cooldown period (ignore speech immediately after TTS)
            if self._speaking_finished_time > 0:
                elapsed = time.time() - self._speaking_finished_time
                if elapsed < 1.0:  # Within 1 second of finishing speech
                    # PART 1: Filter short accidental recognitions
                    words = normalized_input.split()
                    if len(words) <= 2 and any(word in self._short_phrases for word in words):
                        print(f"[Recognition Ignored: echo] '{recognized_text}' (short phrase after TTS)")
                        return True
                    
                    print(f"[Recognition Ignored: cooldown] '{recognized_text}' (within 1s of TTS)")
                    return True
            
            # Check similarity with last spoken text
            if not self._last_spoken_text:
                return False
            
            # Calculate similarity ratio
            similarity = SequenceMatcher(
                None, 
                self._last_spoken_text, 
                normalized_input
            ).ratio()
            
            is_echo_detected = similarity >= similarity_threshold
            
            if is_echo_detected:
                print(f"[Echo Filter] Ignored assistant speech (similarity: {similarity:.2f})")
                print(f"[Echo Filter] Last spoken: '{self._last_spoken_text[:50]}...'")
                print(f"[Echo Filter] Recognized: '{normalized_input[:50]}...'")
            
            return is_echo_detected
    
    def _is_duplicate(self, normalized_text: str) -> bool:
        """
        PART 1: Check if this transcript is a duplicate of a recent one.
        """
        current_time = time.time()
        
        # Clean old entries outside the duplicate window
        while self._transcript_times and current_time - self._transcript_times[0] > self.duplicate_window:
            self._transcript_times.popleft()
            self._recent_transcripts.popleft()
        
        # Check if this exact text appeared recently
        if normalized_text in self._recent_transcripts:
            return True
        
        # Add to recent transcripts
        self._recent_transcripts.append(normalized_text)
        self._transcript_times.append(current_time)
        
        return False
    
    @staticmethod
    def _normalize(text: str) -> str:
        """
        Normalize text for comparison.
        Removes punctuation, extra spaces, and converts to lowercase.
        """
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove common punctuation
        for char in ".,!?;:\"'":
            text = text.replace(char, "")
        
        # Normalize whitespace
        text = " ".join(text.split())
        
        return text


# Global singleton instance
_speaking_state_instance = None
_instance_lock = threading.Lock()


def get_speaking_state() -> SpeakingState:
    """
    Get the global speaking state singleton.
    Thread-safe lazy initialization.
    """
    global _speaking_state_instance
    
    if _speaking_state_instance is None:
        with _instance_lock:
            if _speaking_state_instance is None:
                _speaking_state_instance = SpeakingState()
    
    return _speaking_state_instance
