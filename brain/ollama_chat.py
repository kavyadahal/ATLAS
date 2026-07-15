from ollama import Client
from config import MODEL, HOST


class AtlasBrain:
    def __init__(self):
        self.client = Client(host=HOST)

    def chat(self, message: str) -> str:
        response = self.client.chat(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": message
                }
            ]
        )

        return response["message"]["content"]