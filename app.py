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

    while True:

        if not conversation_mode:
            wake.wait()
            conversation_mode = True

        user = listener.listen(timeout=10)

        if not user:
            print("\nConversation ended.")
            print("Waiting for wake word...\n")
            conversation_mode = False
            continue

        print(f"\nYou : {user}")

        if user.lower() == "exit":
            break

        reply = atlas.chat(user)

        print(f"\nATLAS : {reply}")

        speaker.speak(reply)


if __name__ == "__main__":
    main()