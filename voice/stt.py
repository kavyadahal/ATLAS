from groq import Groq
import os


class SpeechToText:

    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def transcribe(self, audio_file):

        if audio_file is None:
            return ""

        with open(audio_file, "rb") as file:
            response = self.client.audio.transcriptions.create(
                file=file,
                model="whisper-large-v3-turbo",
                language="en"
            )

        return response.text.strip()