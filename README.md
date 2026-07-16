# ATLAS

ATLAS is a local, holographic AI assistant inspired by JARVIS — built from scratch using Python, Ollama, and a Raspberry Pi 4B. It runs entirely on local hardware with no cloud dependency, and is being developed step by step as a real engineering project: identity and personality, long-term memory, voice interaction, and eventually a Pepper's Ghost holographic display.

---

## Features

- ✅ Local AI using Ollama (Qwen 2.5 1.5B)
- ✅ Identity System (ATLAS knows who it is and who created it)
- ✅ Session Conversation History
- ✅ Long-Term Memory (RAG with ChromaDB)
- ✅ Memory Filtering (skips junk/duplicate memories)
- ⏳ Voice Input (Speech-to-Text)
- ⏳ Voice Output (Piper TTS)
- ⏳ Raspberry Pi Integration
- ⏳ Holographic Display (Pepper's Ghost)

---

## Project Structure

```
ATLAS/
│
├── app.py
├── config.py
│
├── brain/
│   ├── __init__.py
│   ├── ollama_chat.py
│   └── identity.py
│
├── memory/
│   ├── __init__.py
│   ├── embeddings.py
│   └── vector_store.py
│
├── data/
│   ├── identity.json
│   └── chroma_db/
│
├── voice/
│
├── avatar/
│
└── assets/
```

**`app.py`**
Entry point of the project. Runs the main input/output loop that lets you talk to ATLAS from the terminal.

**`config.py`**
Stores shared configuration values (like the Ollama model name and host address) used across the project.

**`brain/`**
Handles communication with the AI model and ATLAS's identity/personality logic.
- `ollama_chat.py` — Manages the conversation loop, sends messages to Ollama, and coordinates memory retrieval/storage.
- `identity.py` — Loads ATLAS's identity and builds the system prompt.

**`memory/`**
Contains ATLAS's long-term memory (RAG) system.
- `embeddings.py` — Converts text into embedding vectors using Ollama's `nomic-embed-text` model.
- `vector_store.py` — Saves and searches memories using ChromaDB, and filters near-duplicate memories.

**`data/`**
Stores persistent project data.
- `identity.json` — ATLAS's identity details (name, creator, personality).
- `chroma_db/` — ChromaDB's on-disk database files (auto-created, stores long-term memory vectors).

**`voice/`**
Will contain speech-to-text and text-to-speech logic (Phase 4, not yet started).

**`avatar/`**
Will contain the Blender/holographic avatar rendering and playback logic.

**`assets/`**
Will store static assets used by the avatar/display system (e.g. rendered video/image sequences).

---

## Technologies Used

- **Python** — Core language used to build the entire project.
- **Ollama** — Runs LLMs and embedding models fully locally, no internet required.
- **Qwen 2.5 (1.5B)** — The local language model powering ATLAS's conversation abilities.
- **nomic-embed-text** — Local embedding model used to convert text into vectors for memory search.
- **ChromaDB** — Local vector database used to store and semantically search long-term memories.
- **Raspberry Pi 4B** — Target hardware ATLAS will ultimately run on.
- **Git** — Version control for tracking project progress.
- **VS Code** — Primary development environment.

---

## Installation

Clone the repository:

```bash
git clone <your-repo-url>
cd ATLAS
```

Install Python dependencies:

```bash
pip install ollama chromadb requests
```

Pull the required local models through Ollama:

```bash
ollama pull qwen2.5:1.5b
ollama pull nomic-embed-text
```

---

## Running the Project

Start the Ollama server (skip this if it's already running as a background service):

```bash
ollama serve
```

List installed models to confirm they're available:

```bash
ollama list
```

Run ATLAS:

```bash
python app.py
```

Open a Python shell (useful for testing individual components):

```bash
python
```

Exit the Python shell:

```python
exit()
```

---

## Testing

**Test embedding generation:**

```python
from memory.embeddings import get_embedding

vector = get_embedding("Hello, I am Kavya.")
print(len(vector))   # expected: 768
print(vector[:5])    # expected: first 5 floats of the vector
```

**Test memory storage and semantic search:**

```python
from memory.vector_store import VectorStore

store = VectorStore()
store.add_memory("Sir is building a holographic assistant called ATLAS.")

results = store.search_memories("What is Sir working on?")
print(results)   # expected: the ATLAS-related memory returned, even without exact keyword match
```

**Test memory persistence across restarts:**
Run the search above, restart the Python shell completely, then run only `search_memories` again (without re-adding the memory) — it should still return the same result, proving the data was saved to disk in `data/chroma_db/`.

**Test duplicate/junk filtering:**

```python
from brain.ollama_chat import AtlasBrain

atlas = AtlasBrain()
atlas.chat("ok thanks")   # should NOT be saved (too short)
atlas.chat("My name is Kavya and I study at Deerwalk College in Kathmandu.")
atlas.chat("My name is Kavya and I study at Deerwalk College in Kathmandu.")  # duplicate, should NOT be saved again
```

---

## Development Progress

### Phase 1 - Local AI
- [x] Ollama Installed
- [x] Qwen 2.5 Downloaded
- [x] Python Connected to Ollama
- [x] Local Chat Working

### Phase 2 - Identity
- [x] Identity JSON
- [x] Identity Loader
- [x] System Prompt
- [x] Respectful Responses ("Sir")

### Phase 3 - Long-Term Memory (RAG)
- [x] Embeddings (`nomic-embed-text` via Ollama)
- [x] ChromaDB Persistent Storage
- [x] Semantic Search
- [x] Full RAG Pipeline (retrieve → augment → generate → save)
- [x] Memory Filtering (skip short/junk messages and near-duplicates)

### Phase 4 - Voice Interaction
- [ ] Speech-to-Text (hearing the user)
- [ ] Text-to-Speech (Piper TTS)
- [ ] Voice Loop Integration into `app.py`

### Phase 5 - Raspberry Pi Deployment
- [ ] Move ATLAS onto Raspberry Pi 4B
- [ ] Performance tuning for Pi hardware

### Phase 6 - Holographic Display
- [ ] Pepper's Ghost Physical Build
- [ ] Blender Avatar Rendering Pipeline
- [ ] Avatar Playback Integration

---

## Learning Notes

### Phase 1
Learned:
- Running local LLMs with Ollama
- Basic HTTP-based communication between Python and a local model server
- Structuring a simple Python entry point (`app.py`)

### Phase 2
Learned:
- System prompts and how they shape model behavior
- Reading/writing JSON files in Python
- Classes and objects
- Maintaining conversation history as a list of message dictionaries
- Basic prompt engineering

### Phase 3
Learned:
- What embeddings and vectors are, and how they represent meaning
- What semantic search is and how it differs from keyword search
- Why RAG works: retrieving relevant context instead of relying on the model's fixed memory
- Using ChromaDB as a local, persistent vector database
- Separation of concerns (splitting embedding logic from storage logic into different files)
- Encapsulation (exposing clean methods like `has_memories()` instead of leaking internal details)
- Tuple unpacking and Python's "truthiness" rules for empty lists
- Designing simple heuristics (word count + distance threshold) to filter low-value data

---

## Troubleshooting

### Error
`OSError: [Errno 98] Address already in use` / "Only one usage of each socket address..."

**Solution**
Ollama is already running in the background. Do not run:
```bash
ollama serve
```
Instead, just confirm it's active with:
```bash
ollama list
```

### Error
`ConnectionError` when calling `get_embedding()` or `AtlasBrain.chat()`

**Solution**
Ollama isn't running. Start it with `ollama serve` in a separate terminal, then try again.

### Error
`KeyError: 'embedding'` in `get_embedding()`

**Solution**
The model name passed to Ollama doesn't match an installed model. Run `ollama list` and confirm `nomic-embed-text` is present; if not, run `ollama pull nomic-embed-text`.

---

## Future Roadmap

- [x] RAG Memory
- [ ] Voice Recognition
- [ ] Text-to-Speech
- [ ] Face Recognition
- [ ] Raspberry Pi Sensors
- [ ] Holographic Display
- [ ] Wake Word Detection
- [ ] Vision
- [ ] Internet Search
- [ ] Home Automation

---

## Author

**Creator:** Kabbe
**Project:** ATLAS
