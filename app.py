from brain.ollama_chat import AtlasBrain


def main():
    atlas = AtlasBrain()

    print("=" * 50)
    print("ATLAS AI Assistant")
    print("Type 'exit' to quit")
    print("=" * 50)

    while True:
        user = input("\nYou: ")

        if user.lower() == "exit":
            break

        reply = atlas.chat(user)

        print(f"\nATLAS: {reply}")


if __name__ == "__main__":
    main()