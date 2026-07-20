"""
ATLAS - AI Assistant
Main entry point for the ATLAS assistant system.

Architecture:
- core/atlas.py: Main orchestration
- brain/: Intelligence (chat, intent detection, command execution)
- voice/: Voice I/O (wake word, STT, TTS, listener)
- ui/: User interface (console, input handling)
- commands/: Command registry and implementations
- automation/: System automation (file, desktop, app control)
- memory/: Vector storage and embeddings
"""

from core.atlas import Atlas


def main():
    """Entry point for ATLAS."""
    atlas = Atlas()
    atlas.run()


if __name__ == "__main__":
    main()
