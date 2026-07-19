"""
Local embedding generation using ChromaDB's built-in ONNX models.
No external API calls needed - fully local operation.
"""

from chromadb.utils import embedding_functions


# Initialize the local ONNX embedding function
# This uses the MiniLM-L6-V2 model which is small, fast, and runs locally
embedding_function = embedding_functions.ONNXMiniLM_L6_V2()


def get_embedding(text: str) -> list[float]:
    """
    Converts a piece of text into an embedding vector using a local
    ONNX model (all-MiniLM-L6-v2).

    Args:
        text: The text we want to convert into a vector.

    Returns:
        A list of floats representing the meaning of the text in
        vector space (384 dimensions for MiniLM-L6-V2).
    """
    # The ONNX function expects a list of texts and returns a list of embeddings
    embeddings = embedding_function([text])
    return embeddings[0]
