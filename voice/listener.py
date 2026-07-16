import json
import queue

import sounddevice as sd
import vosk

from config import VOSK_MODEL_PATH

vosk.SetLogLevel(-1)


class Listener:
    """
    Records audio from the microphone on demand and transcribes it to
    text using a local Vosk speech recognition model.
    """

    def __init__(self):
        self.model = vosk.Model(VOSK_MODEL_PATH)
        self.sample_rate = 16000

    def listen(self) -> str:
        audio_queue = queue.Queue()

        def callback(indata, frames, time, status):
            audio_queue.put(bytes(indata))

        recognizer = vosk.KaldiRecognizer(self.model, self.sample_rate)

        with sd.RawInputStream(
            samplerate=self.sample_rate,
            blocksize=8000,
            dtype="int16",
            channels=1,
            callback=callback
        ):
            input()

        while not audio_queue.empty():
            chunk = audio_queue.get()
            recognizer.AcceptWaveform(chunk)

        result = json.loads(recognizer.FinalResult())
        return result.get("text", "")