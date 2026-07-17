import re

import chromadb
from memory.embeddings import get_embedding


class ProfileStore:
    """
    Manages Sir's personal profile (family, education, research, etc.)
    as a separate ChromaDB collection from the auto-remembered
    conversation memories in VectorStore.

    Unlike VectorStore, this is meant to be rebuilt wholesale from
    data/profile.md whenever that file changes, rather than appended to
    incrementally during conversation.
    """

    COLLECTION_NAME = "atlas_profile"

    def __init__(self, path: str = "data/chroma_db"):
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection(
            name=self.COLLECTION_NAME
        )

    def has_profile(self) -> bool:
        return self.collection.count() > 0

    def search_profile(self, query: str, n_results: int = 3) -> list[str]:
        if not self.has_profile():
            return []

        query_embedding = get_embedding(query)
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(n_results, self.collection.count())
        )
        return results["documents"][0]

    def rebuild_from_file(self, path: str = "data/profile.md") -> int:
        """
        Wipes the existing profile collection and re-ingests it from
        the markdown file, chunked by "## Heading" sections. Returns
        the number of chunks stored.
        """

        with open(path, "r", encoding="utf-8") as file:
            text = file.read()

        chunks = self._chunk_markdown(text)

        # Wipe the collection so stale/removed facts don't linger.
        self.client.delete_collection(self.COLLECTION_NAME)
        self.collection = self.client.get_or_create_collection(
            name=self.COLLECTION_NAME
        )

        if not chunks:
            return 0

        ids = [f"profile-{i}" for i in range(len(chunks))]
        embeddings = [get_embedding(chunk) for chunk in chunks]

        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=chunks
        )

        return len(chunks)

    @staticmethod
    def _chunk_markdown(text: str) -> list[str]:
        """
        Splits markdown into one chunk per "## Heading" section, keeping
        the heading attached to its content. Skips empty sections (e.g.
        headings the user left blank) and the top-level instructions.
        """

        sections = re.split(r"(?=^## )", text, flags=re.MULTILINE)

        chunks = []
        for section in sections:
            section = section.strip()

            if not section.startswith("##"):
                continue

            lines = section.splitlines()
            heading = lines[0]
            body_lines = [
                line for line in lines[1:]
                if line.strip() and not line.strip().endswith(":")
            ]

            if not body_lines:
                continue

            chunk = heading + "\n" + "\n".join(body_lines)
            chunks.append(chunk.strip())

        return chunks