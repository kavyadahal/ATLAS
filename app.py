from brain.ollama_chat import AtlasBrain
from voice.listener import Listener
from voice.stt import SpeechToText
from voice.speaker import Speaker
from voice.wake_word import WakeWord


def main():

    atlas = AtlasBrain()
    speaker = Speaker()
    listener = Listener()
    stt = SpeechToText()
    wake = WakeWord()

    conversation_mode = False

    print("=" * 50)
    print("ATLAS")
    print("=" * 50)
    print("Say 'Hey Jarvis' to wake ATLAS.\n")

    try:
        while True:

            if not conversation_mode:
                wake.wait()
                conversation_mode = True

                print("ATLAS : Yes, Sir.\n")
                speaker.speak("Yes, Sir.")
                print("Listening...\n")

            audio_file = listener.listen(timeout=10)

            if audio_file is None:
                print("\nConversation ended.")
                print("Waiting for wake word...\n")
                conversation_mode = False
                continue

            user = stt.transcribe(audio_file)

            if not user:
                print("\n(couldn't understand that)")
                continue

            print(f"You : {user}")

            if user.lower() in ["exit", "quit", "stop"]:
                print("Goodbye, Sir.")
                speaker.speak("Goodbye, Sir.")
                break

            reply = atlas.chat(user)
            print(f"\nATLAS : {reply}\n")
            speaker.speak(reply)

    finally:
        # Release the microphone device cleanly on shutdown, whether we
        # exited normally, via Ctrl+C, or from an unhandled exception.
        wake.close()


if __name__ == "__main__":
    main()