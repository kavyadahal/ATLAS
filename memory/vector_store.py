import chromadb
from memory.embeddings import get_embedding


class VectorStore:
    """
    Manages saving and searching long-term memories using ChromaDB.
    Each memory is stored as text plus its embedding vector.
    """

    def __init__(self, path: str = "data/chroma_db"):
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection(name="atlas_memory")

    def add_memory(self, text: str) -> None:
        embedding = get_embedding(text)
        next_id = str(self.collection.count())
        self.collection.add(
            ids=[next_id],
            embeddings=[embedding],
            documents=[text]
        )

    def search_memories(self, query: str, n_results: int = 3) -> list[str]:
        query_embedding = get_embedding(query)
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        return results["documents"][0]

    def has_memories(self) -> bool:
        return self.collection.count() > 0

    def find_closest(self, text: str) -> tuple[str, float] | None:
        if not self.has_memories():
            return None

        embedding = get_embedding(text)
        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=1
        )

        closest_text = results["documents"][0][0]
        closest_distance = results["distances"][0][0]

        return closest_text, closest_distance