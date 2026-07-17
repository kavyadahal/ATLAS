import chromadb
from chromadb.utils import embedding_functions


class VectorStore:
    """
    Manages saving and searching long-term memories using ChromaDB.
    Embeddings are handled by ChromaDB's default local model (no Ollama).
    """

    def __init__(self, path: str = "data/chroma_db"):
        self.client = chromadb.PersistentClient(path=path)
        self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.client.get_or_create_collection(
            name="atlas_memory",
            embedding_function=self.embedding_fn,
        )

    def add_memory(self, text: str) -> None:
        next_id = str(self.collection.count())
        self.collection.add(ids=[next_id], documents=[text])

    def search_memories(self, query: str, n_results: int = 3) -> list[str]:
        results = self.collection.query(query_texts=[query], n_results=n_results)
        return results["documents"][0]

    def has_memories(self) -> bool:
        return self.collection.count() > 0

    def find_closest(self, text: str) -> tuple[str, float] | None:
        if not self.has_memories():
            return None

        results = self.collection.query(query_texts=[text], n_results=1)

        closest_text = results["documents"][0][0]
        closest_distance = results["distances"][0][0]

        return closest_text, closest_distance
