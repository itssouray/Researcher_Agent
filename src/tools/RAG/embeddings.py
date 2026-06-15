from sentence_transformers import SentenceTransformer


class EmbeddingModel:

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        
        self.model = SentenceTransformer(
            model_name
        )

    def embed_text(self, text: str) -> list[float]:
        return self.model.encode(
            text,
            convert_to_numpy=True
        )

    def embed_documents(
        self,
        documents: list[str]
    ):
        return self.model.encode(
            documents,
            convert_to_numpy=True
        )