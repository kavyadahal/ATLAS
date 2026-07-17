# ATLAS

ATLAS is an AI voice assistant built with Python. It uses **Groq** for AI responses, **Vosk** for speech recognition, and **Piper** for text-to-speech.

## Requirements

Before getting started, make sure you have:

* Python 3.10 or later installed
* Git installed
* A Groq API key from https://console.groq.com/keys
* An internet connection (to download packages/models and call Groq)

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

## Step 3: Download the AI Voice Models

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

## Step 4: Add your Groq API key

Copy the example env file and put your key in it:

```bash
copy .env.example .env
```

Then edit `.env` and replace `your_groq_api_key_here` with your real key:

```
GROQ_API_KEY=gsk_...
```

Optional: change the model with `GROQ_MODEL` (default is `llama-3.1-8b-instant`).

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
├── brain/
├── data/
├── memory/
├── voice/
├── install.bat
├── download_models.bat
├── run.bat
├── requirements.txt
├── README.md
└── app.py
```

---

# Troubleshooting

### Python is not recognized

Make sure Python is installed and added to your system PATH.

---

### GROQ_API_KEY is missing

Create a `.env` file in the ATLAS folder (see `.env.example`) and set `GROQ_API_KEY`.

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
* Groq
* Vosk
* Piper
* ChromaDB

---

# License

This project is intended for learning and personal use.
