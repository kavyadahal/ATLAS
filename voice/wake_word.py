import time

import sounddevice as sd

from openwakeword.model import Model


class WakeWord:
    """
    Continuously listens for the wake word.

    Returns True when the wake word is detected.
    """

    def __init__(self):

        self.sample_rate = 16000

        # Uses the default OpenWakeWord model.
        # We'll replace this with a custom "Hey ATLAS"
        # model later.
        self.model = Model()

    def wait(self):

        print("Waiting for wake word...")

        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype="float32",
        ) as stream:

            while True:

                audio, overflowed = stream.read(1280)

                prediction = self.model.predict(audio)

                for score in prediction.values():

                    if score > 0.5:

                        print("Wake word detected.\n")

                        time.sleep(0.3)

                        return True