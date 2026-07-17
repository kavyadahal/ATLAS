import numpy as np
from openwakeword.model import Model
from pvrecorder import PvRecorder


class WakeWord:
    """
    Listens continuously for the wake word using OpenWakeWord.
    Returns only after the wake word has been detected.
    """

    def __init__(self):

        self.model = Model(
            wakeword_models=["hey_jarvis"],
            inference_framework="onnx"
        )

        self.recorder = PvRecorder(
            device_index=-1,
            frame_length=1280
        )

    def wait(self):

        print("Waiting for wake word...")

        self.recorder.start()

        try:

            while True:

                pcm = self.recorder.read()

                audio = np.array(
                    pcm,
                    dtype=np.int16
                )

                prediction = self.model.predict(audio)

                score = prediction.get("hey_jarvis", 0)

                if score > 0.5:

                    print("\nWake word detected!\n")

                    break

        finally:

            self.recorder.stop()