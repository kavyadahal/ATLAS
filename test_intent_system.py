"""
Test script to verify intent detection and execution system.
"""

from brain.intent_detector import IntentDetector

def test_intents():
    """Test various user inputs to verify intent detection."""
    
    detector = IntentDetector()
    
    test_cases = [
        # File creation commands
        "create a text file on my desktop",
        "create file",
        "create hello.txt",
        "make a file called test.txt",
        "create notes.txt on desktop",
        "create a python file called test.py",
        "new file named example.txt",
        
        # Folder commands
        "create a folder on my desktop",
        "make folder called MyFolder",
        
        # File operations (BUG FIXES)
        "open kavya.py",  # Should be OPEN_FILE not OPEN_APP
        "open app.py",    # Should be OPEN_FILE not OPEN_APP
        "open notes.txt", # Should be OPEN_FILE not OPEN_APP
        "read app.py",
        "edit config.json",
        "delete app.py",  # Should be DELETE_FILE not chat
        "delete notes.txt",
        "run app.py",
        
        # App commands (should NOT match files)
        "open chrome",    # Should be OPEN_APP
        "open vscode",    # Should be OPEN_APP
        "open notepad",
        "close chrome",
        
        # Conversational queries (should be 'chat')
        "what is python",
        "who are you",
        "explain machine learning",
        "how are you",
        "tell me about AI",
    ]
    
    print("=" * 70)
    print("INTENT DETECTION TEST")
    print("=" * 70)
    
    for test_input in test_cases:
        intent, params = detector.detect_intent(test_input)
        print(f"\nInput: '{test_input}'")
        print(f"Intent: {intent}")
        if params:
            print(f"Params: {params}")
        print("-" * 70)

if __name__ == "__main__":
    test_intents()
