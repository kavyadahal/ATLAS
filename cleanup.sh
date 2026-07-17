#!/usr/bin/env bash
# Run this from inside your ATLAS project root (where app.py lives).
# Removes files that are unused, duplicated, or shouldn't be committed/shared.

set -e

echo "Removing unused Vosk STT model (68MB, unused now that Groq Whisper handles STT)..."
rm -rf voice/vosk-model-small-en-us-0.15

echo "Removing duplicate/orphaned Chroma DB at project root (the real one lives in data/chroma_db)..."
rm -rf chroma_db

echo "Removing empty/unused stub file brain/rag.py (never imported anywhere)..."
rm -f brain/rag.py

echo "Removing all __pycache__ folders and .pyc files..."
find . -type d -name "__pycache__" -not -path "./.venv/*" -exec rm -rf {} +
find . -type f -name "*.pyc" -not -path "./.venv/*" -delete

echo "Removing the .venv folder (huge, machine-specific, regenerate via insall.bat/install.bat)..."
rm -rf .venv

echo "Done. Also remember to:"
echo "  1. Rotate your Groq API key (it was exposed in .env) at console.groq.com/keys"
echo "  2. Rename insall.bat -> install.bat (typo)"
echo "  3. Never commit/zip .env or .venv again -- they're already in .gitignore"