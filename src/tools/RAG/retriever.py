import numpy as np

from src.tools.RAG.embeddings import EmbeddingModel
from src.tools.RAG.vector_store import VectorStore


class Retriever:

    def __init__(self):

        self.embedding_model = EmbeddingModel()
        self.vector_store = VectorStore()

        self.index, self.metadata = (
            self.vector_store.load()
        )

    def retrieve(
        self,
        query: str,
        k: int = 5
    ):

        query_embedding = (
            self.embedding_model
            .embed_text(query)
            .astype("float32")
            .reshape(1, -1)
        )

        distances, indices = (
            self.index.search(
                query_embedding,
                k
            )
        )

        results = []

        for idx, distance in zip(indices[0], distances[0]):

            results.append(
                {
                    **self.metadata[idx],
                    "score": float(distance)
                }
            )

        return results