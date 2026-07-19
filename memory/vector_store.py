import chromadb
from chromadb.utils import embedding_functions


class VectorStore:
    """
    Manages saving and searching long-term memories using ChromaDB.
    Each memory is stored as text plus its embedding vector.
    Uses local ONNX embeddings (384 dimensions).
    """

    def __init__(self, path: str = "data/chroma_db"):
        self.client = chromadb.PersistentClient(path=path)
        
        # Use local ONNX embedding function
        self.embedding_function = embedding_functions.ONNXMiniLM_L6_V2()
        
        # Get or create collection with the ONNX embedding function
        # This ensures the collection uses the correct embedding dimensions (384)
        self.collection = self.client.get_or_create_collection(
            name="atlas_memory_onnx",  # New collection name to avoid dimension mismatch
            embedding_function=self.embedding_function
        )

    def add_memory(self, text: str) -> None:
        """Add a memory to the vector store. ChromaDB handles embedding automatically."""
        next_id = str(self.collection.count())
        self.collection.add(
            ids=[next_id],
            documents=[text]
        )

    def search_memories(self, query: str, n_results: int = 3) -> list[str]:
        """Search for relevant memories. ChromaDB handles query embedding automatically."""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results["documents"][0] if results["documents"] else []

    def has_memories(self) -> bool:
        """Check if any memories exist."""
        return self.collection.count() > 0

    def find_closest(self, text: str) -> tuple[str, float] | None:
        """Find the closest matching memory. ChromaDB handles embedding automatically."""
        if not self.has_memories():
            return None

        results = self.collection.query(
            query_texts=[text],
            n_results=1
        )

        if results["documents"] and results["documents"][0]:
            closest_text = results["documents"][0][0]
            closest_distance = results["distances"][0][0]
            return closest_text, closest_distance
        
        return None
