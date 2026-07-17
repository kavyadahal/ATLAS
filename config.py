import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Fast Groq model — swap for llama-3.3-70b-versatile if you want higher quality
MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

VOICE_MODEL_PATH = "voice/en_US-ryan-high.onnx"

VOSK_MODEL_PATH = "voice/vosk-model-small-en-us-0.15"
