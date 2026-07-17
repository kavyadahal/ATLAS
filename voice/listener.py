import queue
import time

import numpy as np
import sounddevice as sd
import soundfile as sf


class Listener:

    def __init__(self, sample_rate=16000, silence_threshold=500, silence_timeout=1.5):
        self.sample_rate = sample_rate
        self.silence_threshold = silence_threshold  # RMS level below which = "quiet"
        self.silence_timeout = silence_timeout       # seconds of quiet before stopping

    def listen(self, timeout=10, filename="input.wav"):
        """
        Records from the mic until the user stops talking (or times out
        with no speech at all). Returns a path to the wav file, or None
        if nothing was said.
        """

        audio_queue = queue.Queue()

        def callback(indata, frames, time_info, status):
            if status:
                print(status)
            audio_queue.put(indata.copy())

        print("Listening...")

        frames = []
        start_time = time.time()
        last_voice_time = time.time()
        speech_started = False

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
                        return None
                    continue

                frames.append(block)

                rms = np.sqrt(np.mean(block.astype(np.float32) ** 2))

                if rms > self.silence_threshold:
                    if not speech_started:
                        print("Hearing you...")
                    speech_started = True
                    last_voice_time = time.time()

                if speech_started and time.time() - last_voice_time > self.silence_timeout:
                    break

                if not speech_started and time.time() - start_time > timeout:
                    return None

        if not speech_started:
            return None

        audio = np.concatenate(frames, axis=0)
        sf.write(filename, audio, self.sample_rate)

        return filename