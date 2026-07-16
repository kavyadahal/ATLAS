# ATLAS

ATLAS is a local AI voice assistant built with Python. It uses **Ollama** for AI responses, **Vosk** for speech recognition, and **Piper** for text-to-speech.

## Requirements

Before getting started, make sure you have:

* Python 3.10 or later installed
* Git installed
* Ollama installed and running
* An internet connection (to download required packages and models)

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

## Step 4: Install Ollama

Download and install Ollama from:

https://ollama.com/download

After installation, start Ollama.

Pull the model used by ATLAS (replace with your preferred model if needed):

```bash
ollama pull llama3.2
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

### Ollama is not running

Start the Ollama application before launching ATLAS.

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
* Ollama
* Vosk
* Piper
* ChromaDB

---

# License

This project is intended for learning and personal use.
