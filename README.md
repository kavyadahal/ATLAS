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


## Capabilities Added

### 1. **Explain Files**
```
User: "Explain app.py"
ATLAS: [Reads file, analyzes structure, provides AI explanation]

User: "Open listener.py and explain it"
ATLAS: [Reads listener.py, explains architecture and functionality]

User: "What does config.py do?"
ATLAS: [Analyzes and explains config.py]
```

### 2. **Read and Understand Files**
- Reads any text/code file up to 1MB
- Analyzes structure (functions, classes, imports)
- Provides intelligent explanations via Groq AI
- Handles Python, JavaScript, HTML, CSS, JSON, etc.

### 3. **Generate Code**
```
User: "Write a simple hello world program in test.py"
ATLAS: [Generates code, writes to test.py, confirms]

User: "Write a calculator in calc.py"
ATLAS: [Generates full calculator code via AI]
```

### 4. **Append Code**
```
User: "Add a function to utils.py that calculates factorial"
ATLAS: [Generates factorial function, appends to utils.py]

User: "Add error handling to logger.py"
ATLAS: [Generates error handling code, appends]
```

### 5. **Replace Functions**
```
User: "Replace the login() function in auth.py with a better version"
ATLAS: [Finds login(), generates improved version, replaces it]

User: "Update the validate() function in validator.py"
ATLAS: [Locates function, generates replacement, updates file]
```

### 6. **Insert Code**
```
User: "Insert logging code in processor.py"
ATLAS: [Generates logging code, inserts at appropriate location]
```

### 7. **Overwrite Files**
```
User: "Completely rewrite test.py as a unit test suite"
ATLAS: [Generates new content, overwrites entire file]
```

---

