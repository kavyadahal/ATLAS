import requests


def get_embedding(text: str) -> list[float]:
    """
    Converts a piece of text into an embedding vector using Ollama's
    local nomic-embed-text model.

    Args:
        text: The text we want to convert into a vector.

    Returns:
        A list of floats representing the meaning of the text in
        vector space (typically 768 numbers for nomic-embed-text).
    """
    response = requests.post(
        "http://localhost:11434/api/embeddings",
        json={
            "model": "nomic-embed-text",
            "prompt": text
        }
    )
    response.raise_for_status()
    data = response.json()
    return data["embedding"]