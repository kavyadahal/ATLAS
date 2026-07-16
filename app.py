from brain.ollama_chat import AtlasBrain
from voice.speaker import Speaker
from voice.listener import Listener


def main():

    atlas = AtlasBrain()
    speaker = Speaker()
    listener = Listener()

    print("=" * 50)
    print("ATLAS")
    print("=" * 50)

    while True:

        input("\nPress Enter to speak, then press Enter again when done...")
        print("Listening...")

        user = listener.listen()

        if not user:
            print("(Didn't catch that, Sir.)")
            continue

        print(f"You : {user}")

        if user.lower() == "exit":
            break

        reply = atlas.chat(user)

        print(f"\nATLAS : {reply}")
        speaker.speak(reply)


if __name__ == "__main__":
    main()