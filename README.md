# ATLAS v2 – AI Operating System

ATLAS is a cloud-powered AI voice assistant built with Python that includes **desktop control** and **smart file management** capabilities. It uses **Groq** for AI responses and embeddings via **Gemini**, **Vosk** for speech recognition, and **Piper** for text-to-speech.

## 🆕 What's New in v2

ATLAS has evolved from a simple voice assistant into an AI Operating System with:

- **Desktop Control**: Open/close applications, manage windows, browse websites
- **Smart File System**: Search, organize, manage files with natural language
- **Safety First**: Confirmation required for dangerous operations
- **Comprehensive Logging**: All operations tracked with timestamps
- **Seamless Integration**: Works alongside existing conversational AI
- **Cloud-Powered**: No local LLM required - runs entirely on cloud APIs

👉 **[Read the Full Automation Guide](AUTOMATION_GUIDE.md)**

## Requirements

Before getting started, make sure you have:

* Python 3.10 or later installed
* Git installed
* A **Groq API key** (get one free at [console.groq.com](https://console.groq.com))
* An internet connection

---

# Installation

## Step 1: Clone the repository

```bash
git clone https://github.com/kavyadahal/ATLAS.git
cd ATLAS
```

---

## Step 2: Install ATLAS

Simply double-click:

```
install.bat
```

This will automatically:

* Create a virtual environment
* Upgrade pip
* Install all required Python packages

Wait until the installation finishes.

---

## Step 3: Configure API Keys

Create a `.env` file in the project root with your API keys:

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

**Where to get API key:**
- **Groq API Key**: Sign up at [console.groq.com](https://console.groq.com) (free tier available)

**Optional**: Set `GROQ_MODEL` to use a different model. Default is `llama-3.3-70b-versatile`.

---

## Step 4: Download the AI Voice Models

Double-click:

```
download_models.bat
```

Follow the instructions shown in the terminal.

Download and place the models inside the `voice` folder as instructed.

Your folder should look like this:

```
voice/
│
├── en_US-ryan-high.onnx
├── en_US-ryan-high.onnx.json
└── vosk-model-small-en-us-0.15/
```

---

## Step 5: Run ATLAS

Double-click:

```
run.bat
```

ATLAS will start listening for your voice.

---

# Updating the Project

Whenever you download a newer version:

1. Pull the latest changes.

```bash
git pull
```

2. If new packages were added, run:

```
install.bat
```

again.

---

# Project Structure

```
ATLAS/
│
├── automation/          # Desktop & file control modules
├── brain/              # AI chat logic
├── data/               # Identity and profile data
├── memory/             # Vector store & embeddings
├── voice/              # Speech recognition & TTS
├── install.bat
├── download_models.bat
├── run.bat
├── requirements.txt
├── README.md
├── AUTOMATION_GUIDE.md
└── app.py
```

---

# Troubleshooting

### Python is not recognized

Make sure Python is installed and added to your system PATH.

---

### API Key errors

Make sure you have created a `.env` file with valid `GROQ_API_KEY`.

---

### Voice models not found

Make sure the following files exist:

```
voice/
├── en_US-ryan-high.onnx
├── en_US-ryan-high.onnx.json
└── vosk-model-small-en-us-0.15/
```

---

# Technologies Used

* Python
* Groq (LLM API)
* Local ONNX Embeddings (via ChromaDB)
* Vosk (Speech-to-Text)
* Piper (Text-to-Speech)
* ChromaDB (Vector Database)

---

# Architecture

- **Chat Generation**: Groq API with `llama-3.3-70b-versatile` (configurable)
- **Embeddings**: Local ONNX embeddings (all-MiniLM-L6-v2) - no API key required
- **Memory**: ChromaDB for long-term memory with RAG
- **Voice**: Local Vosk STT + Piper TTS
- **Automation**: Native Windows desktop and file system control

---

# License

This project is intended for learning and personal use.
