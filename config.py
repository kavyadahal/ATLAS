import os
from dotenv import load_dotenv

load_dotenv()

# AI Provider Configuration
AI_PROVIDER = "groq"

# Groq (Chat Generation & Whisper STT)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
STT_MODEL = "llama-3.3-70b-versatile"

# Embeddings - Local ONNX (no API key needed)
# Using ChromaDB's built-in all-MiniLM-L6-v2 model

# Piper TTS
VOICE_MODEL_PATH = "voice/en_US-ryan-high.onnx"
