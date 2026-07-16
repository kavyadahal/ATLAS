import io
import wave

from piper import PiperVoice, SynthesisConfig
import simpleaudio as sa

from config import VOICE_MODEL_PATH


SPEECH_LENGTH_SCALE = 1.15
STARTUP_SILENCE_SECONDS = 0.3


class Speaker:
    """
    Converts text into spoken audio using a local Piper TTS voice model,
    and plays it through the system's speakers.
    """

    def __init__(self):
        self.voice = PiperVoice.load(VOICE_MODEL_PATH)
        self.syn_config = SynthesisConfig(length_scale=SPEECH_LENGTH_SCALE)

    def speak(self, text: str) -> None:
        buffer = io.BytesIO()

        with wave.open(buffer, "wb") as wav_file:
            self.voice.synthesize_wav(text, wav_file, syn_config=self.syn_config)

        buffer.seek(0)


        with wave.open(buffer, "rb") as wav_reader:
            channels = wav_reader.getnchannels()
            sample_width = wav_reader.getsampwidth()
            frame_rate = wav_reader.getframerate()
            audio_frames = wav_reader.readframes(wav_reader.getnframes())

        silence_frame_count = int(frame_rate * STARTUP_SILENCE_SECONDS)
        silence_bytes = b"\x00" * (silence_frame_count * channels * sample_width)

        padded_audio = silence_bytes + audio_frames

        play_obj = sa.play_buffer(padded_audio, channels, sample_width, frame_rate)
        play_obj.wait_done()