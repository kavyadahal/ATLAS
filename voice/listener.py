import queue
import time
import uuid
import os

import numpy as np
import sounddevice as sd
import soundfile as sf

from voice.speaking_state import get_speaking_state


class Listener:

    def __init__(self, sample_rate=16000, silence_threshold=500, silence_timeout=1.5):
        self.sample_rate = sample_rate
        self.silence_threshold = silence_threshold  # RMS level below which = "quiet"
        self.silence_timeout = silence_timeout       # seconds of quiet before stopping
        self.recognition_counter = 0  # Track recognition events

    def listen(self, timeout=10, filename="input.wav", silent=False):
        """
        Records from the mic until the user stops talking (or times out
        with no speech at all). Returns a path to the wav file, or None
        if nothing was said.
        
        Args:
            timeout: Maximum time to wait for speech to start (seconds)
            filename: Output WAV file path (will be made unique)
            silent: If True, suppress print statements for background operation
        
        Returns:
            Tuple of (audio_file_path, recognition_id) or (None, None) if no speech
        """
        speaking_state = get_speaking_state()
        
        # Generate unique recognition ID
        self.recognition_counter += 1
        recognition_id = f"REC_{self.recognition_counter}_{int(time.time() * 1000)}"
        
        # CRITICAL: Wait until TTS finishes before accepting microphone input
        if speaking_state.is_speaking():
            if not silent:
                print(f"[{recognition_id}] Paused (assistant speaking)")
            speaking_state.wait_until_can_listen()
        
        if not silent:
            print(f"[{recognition_id}] Listening...")

        # Create unique filename to prevent file reuse
        base_name, ext = os.path.splitext(filename)
        unique_filename = f"{base_name}_{recognition_id}{ext}"
        
        audio_queue = queue.Queue()

        def callback(indata, frames, time_info, status):
            if status and not silent:
                print(f"[{recognition_id}] Audio status: {status}")
            audio_queue.put(indata.copy())

        frames = []
        start_time = time.time()
        last_voice_time = time.time()
        speech_started = False

        # CRITICAL: Add 100ms delay before starting stream to ensure microphone buffer is clear
        time.sleep(0.1)

        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype="int16",
            blocksize=4000,
            callback=callback
        ):
            while True:
                try:
                    block = audio_queue.get(timeout=0.1)
                except queue.Empty:
                    if not speech_started and time.time() - start_time > timeout:
                        if not silent:
                            print(f"[{recognition_id}] ❌ Timeout - No speech detected")
                        return None, None
                    continue

                frames.append(block)

                rms = np.sqrt(np.mean(block.astype(np.float32) ** 2))

                if rms > self.silence_threshold:
                    speech_started = True
                    last_voice_time = time.time()
                    if not silent:
                        print(f"[{recognition_id}] 🎤 Speech detected (RMS: {rms:.0f})")

                if speech_started and time.time() - last_voice_time > self.silence_timeout:
                    if not silent:
                        print(f"[{recognition_id}] ✓ Speech ended")
                    break

                if not speech_started and time.time() - start_time > timeout:
                    if not silent:
                        print(f"[{recognition_id}] ❌ Timeout - No speech detected")
                    return None, None

        if not speech_started:
            if not silent:
                print(f"[{recognition_id}] ❌ No speech detected")
            return None, None

        # CRITICAL: Ensure the queue is fully drained
        while not audio_queue.empty():
            try:
                audio_queue.get_nowait()
            except queue.Empty:
                break

        if not silent:
            print(f"[{recognition_id}] 💾 Saving audio ({len(frames)} frames)...")

        audio = np.concatenate(frames, axis=0)
        sf.write(unique_filename, audio, self.sample_rate)

        if not silent:
            print(f"[{recognition_id}] ✓ Saved to {unique_filename}")

        return unique_filename, recognition_id
    
    def cleanup_old_files(self, pattern="input_*.wav"):
        """Clean up old audio files to prevent disk bloat."""
        import glob
        for file in glob.glob(pattern):
            try:
                os.remove(file)
            except:
                pass
