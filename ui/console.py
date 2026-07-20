"""
Console Output Module
Handles all console output formatting and thread-safe printing.
"""

import threading


class Console:
    """Manages console output with thread-safe printing."""
    
    def __init__(self):
        """Initialize console with output lock."""
        self.output_lock = threading.Lock()
    
    def print_header(self):
        """Print the professional ATLAS header."""
        with self.output_lock:
            print("\n" + "=" * 50)
            print(" " * 17 + "A T L A S")
            print("=" * 50)
            print()
            print("Status      : 🟢 Listening")
            print("Wake Word   : Enabled")
            print("Memory      : Connected")
            print("AI          : Groq")
            print()
            print("-" * 50)
            print()
    
    def print_prompt(self):
        """Print the user input prompt."""
        with self.output_lock:
            print("\nYou : ", end='', flush=True)
    
    def print_response(self, text: str):
        """Print ATLAS response."""
        with self.output_lock:
            print(f"\n\nATLAS : {text}")
    
    def print_message(self, text: str):
        """Print a general message."""
        with self.output_lock:
            print(text, flush=True)
    
    def print_debug(self, text: str):
        """Print debug message."""
        with self.output_lock:
            print(f"[DEBUG] {text}", flush=True)
