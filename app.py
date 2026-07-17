from brain.ollama_chat import AtlasBrain
from voice.listener import Listener
from voice.speaker import Speaker
from voice.wake_word import WakeWord


def main():

    atlas = AtlasBrain()
    speaker = Speaker()
    listener = Listener()
    wake = WakeWord()

    conversation_mode = False

    print("=" * 50)
    print("ATLAS")
    print("=" * 50)
    print("Say 'Hey Jarvis' to wake ATLAS.\n")

    while True:

        # Wait for wake word if ATLAS is sleeping
        if not conversation_mode:
            wake.wait()
            conversation_mode = True
            print("Listening...\n")

        # Listen for the user's command
        user = listener.listen(timeout=5)

        # If the user stays silent, go back to sleep
        if not user:
            print("\nConversation ended.")
            print("Waiting for wake word...\n")
            conversation_mode = False
            continue

        print(f"You : {user}")

        # Exit command
        if user.lower() == "exit":
            print("Goodbye, Sir.")
            break

        # Generate AI response
        reply = atlas.chat(user)

        print(f"\nATLAS : {reply}")

        # Speak response
        speaker.speak(reply)


if __name__ == "__main__":
    main()