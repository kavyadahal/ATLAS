import os
from dotenv import load_dotenv

load_dotenv()

# Ollama (local LLM brain)
MODEL = "qwen2.5:1.5b"
HOST = "http://localhost:11434"

# Piper TTS
VOICE_MODEL_PATH = "voice/en_US-ryan-high.onnx"

# Groq (Whisper STT)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
STT_MODEL = "whisper-large-v3-turbo"