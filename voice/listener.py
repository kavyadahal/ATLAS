import json
import queue
import time

import sounddevice as sd
import vosk

from config import VOSK_MODEL_PATH

vosk.SetLogLevel(-1)


class Listener:
    """
    Records speech from the microphone until the user
    stops talking for a short period.

    If timeout is provided, ATLAS waits only that many
    seconds for the user to START speaking.

    Returns:
        str: Recognized speech.
    """

    def __init__(self):

        self.model = vosk.Model(VOSK_MODEL_PATH)
        self.sample_rate = 16000

        # Create one recognizer and reuse it.
        self.recognizer = vosk.KaldiRecognizer(
            self.model,
            self.sample_rate
        )

    def listen(self, timeout=None) -> str:

        audio_queue = queue.Queue()

        def callback(indata, frames, time_info, status):
            if status:
                print(status)

            audio_queue.put(bytes(indata))

        # Reset recognizer for a fresh sentence
        self.recognizer.Reset()

        print("Listening...")

        # Time allowed after user stops speaking
        silence_timeout = 1.2

        # Tracks last detected speech
        last_voice_time = time.time()

        # Tracks when we started waiting
        start_time = time.time()

        # Has the user started speaking yet?
        speech_started = False

        # Small microphone warm-up
        time.sleep(0.3)

        with sd.RawInputStream(
            samplerate=self.sample_rate,
            blocksize=2000,
            dtype="int16",
            channels=1,
            callback=callback,
        ):

            while True:

                # Wait briefly for microphone data.
                try:
                    data = audio_queue.get(timeout=0.1)

                except queue.Empty:

                    # User never started speaking.
                    if (
                        timeout is not None
                        and not speech_started
                        and time.time() - start_time > timeout
                    ):
                        return ""

                    continue

                # Process audio.
                if self.recognizer.AcceptWaveform(data):

                    result = json.loads(
                        self.recognizer.Result()
                    )

                    text = result.get("text", "").strip()

                    if text:
                        speech_started = True
                        last_voice_time = time.time()

                else:

                    partial = json.loads(
                        self.recognizer.PartialResult()
                    )

                    if partial.get("partial"):

                        speech_started = True
                        last_voice_time = time.time()

                # Stop after user has been silent.
                if (
                    speech_started
                    and time.time() - last_voice_time > silence_timeout
                ):
                    break

        result = json.loads(
            self.recognizer.FinalResult()
        )

        return result.get("text", "").strip()