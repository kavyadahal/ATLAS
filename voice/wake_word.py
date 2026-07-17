import json
import queue
import time

import sounddevice as sd
import vosk

from config import VOSK_MODEL_PATH

vosk.SetLogLevel(-1)


class WakeWord:
    """
    Continuously listens for the wake word 'hey atlas'.

    When the wake word is detected, it returns True.
    """

    def __init__(self):
        self.model = vosk.Model(VOSK_MODEL_PATH)
        self.sample_rate = 16000

    def wait(self) -> bool:

        audio_queue = queue.Queue()

        def callback(indata, frames, time, status):
            audio_queue.put(bytes(indata))

        recognizer = vosk.KaldiRecognizer(
            self.model,
            self.sample_rate
        )

        with sd.RawInputStream(
            samplerate=self.sample_rate,
            blocksize=8000,
            dtype="int16",
            channels=1,
            callback=callback
        ):

            print("Waiting for wake word...")

            while True:

                data = audio_queue.get()

                if recognizer.AcceptWaveform(data):

                    result = json.loads(
                        recognizer.Result()
                    )

                    text = result.get("text", "").lower()

                    if text:
                        print(f"Heard: {text}")

                    if "hey atlas" in text:
                        print("Wake word detected.\n")
                        time.sleep(0.3)
                        return True