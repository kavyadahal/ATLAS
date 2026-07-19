import numpy as np

from openwakeword.model import Model
from pvrecorder import PvRecorder


class WakeWord:

    def __init__(self):

        self.model = Model(
            wakeword_models=["hey_jarvis"],
            inference_framework="onnx"
        )

        self.recorder = PvRecorder(
            device_index=-1,
            frame_length=1280
        )

    def wait(self, silent=False):
        """
        Blocks until the wake word is detected. Can be called repeatedly
        across multiple conversation cycles (the recorder is only started
        and stopped here, never deleted, so it stays reusable).
        
        Args:
            silent: If True, suppress print statements for background operation
        """

        if not silent:
            print("Waiting for wake word...")

        self.recorder.start()

        try:
            while True:
                pcm = self.recorder.read()
                audio = np.array(pcm, dtype=np.int16)

                prediction = self.model.predict(audio)
                score = prediction.get("hey_jarvis", 0)

                if score > 0.5:
                    if not silent:
                        print("\nWake word detected!\n")
                    break

        finally:
            # Only stop here — do NOT delete. Deleting destroys the
            # underlying recorder object, so any future call to wait()
            # would crash on self.recorder.start().
            self.recorder.stop()

    def close(self):
        """
        Call this once when the whole program is shutting down (e.g. in
        a try/finally around main(), or on Ctrl+C) to release the mic
        device cleanly. Do NOT call this between conversation cycles.
        """
        self.recorder.delete()