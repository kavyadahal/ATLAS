from groq import Groq
import os
import time


class SpeechToText:

    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.last_transcription = None
        self.last_transcription_time = 0

    def transcribe(self, audio_file, recognition_id="UNKNOWN"):
        """
        Transcribe audio file to text.
        
        Args:
            audio_file: Path to audio file, or None
            recognition_id: Unique ID for this recognition event
            
        Returns:
            Transcribed text or empty string
        """
        print(f"[{recognition_id}] 🔄 Starting transcription...")
        
        if audio_file is None:
            print(f"[{recognition_id}] ⚠️ No audio file provided")
            return ""

        if not os.path.exists(audio_file):
            print(f"[{recognition_id}] ❌ Audio file does not exist: {audio_file}")
            return ""

        try:
            file_size = os.path.getsize(audio_file)
            print(f"[{recognition_id}] 📁 File size: {file_size} bytes")
            
            with open(audio_file, "rb") as file:
                response = self.client.audio.transcriptions.create(
                    file=file,
                    model="whisper-large-v3-turbo",
                    language="en"
                )

            transcript = response.text.strip()
            current_time = time.time()
            
            # Check if this is a duplicate transcription
            if (transcript == self.last_transcription and 
                current_time - self.last_transcription_time < 3.0):
                print(f"[{recognition_id}] ⚠️ DUPLICATE TRANSCRIPT DETECTED!")
                print(f"[{recognition_id}] Previous: '{self.last_transcription}' ({current_time - self.last_transcription_time:.1f}s ago)")
            
            self.last_transcription = transcript
            self.last_transcription_time = current_time
            
            print(f"[{recognition_id}] ✓ Transcript: '{transcript}'")
            
            # CRITICAL: Delete the audio file immediately after transcription
            try:
                os.remove(audio_file)
                print(f"[{recognition_id}] 🗑️ Audio file deleted")
            except Exception as e:
                print(f"[{recognition_id}] ⚠️ Failed to delete audio file: {e}")
            
            return transcript
            
        except Exception as e:
            print(f"[{recognition_id}] ❌ Transcription error: {e}")
            return ""
