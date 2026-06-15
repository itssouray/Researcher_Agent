import faiss
import pickle
import numpy as np
from pathlib import Path


class VectorStore:

    def __init__(
        self,
        db_path: str = "data/vectordb"
    ):
        self.db_path = Path(db_path)

        self.index_file = (
            self.db_path / "knowledge_base.faiss"
        )

        self.metadata_file = (
            self.db_path / "metadata.pkl"
        )

    def create_index(
        self,
        embeddings: np.ndarray
    ):
        dimension = embeddings.shape[1]

        index = faiss.IndexFlatL2(
            dimension
        )

        index.add(embeddings)

        return index

    def save(
        self,
        index,
        metadata
    ):
        self.db_path.mkdir(
            parents=True,
            exist_ok=True
        )

        faiss.write_index(
            index,
            str(self.index_file)
        )

        with open(
            self.metadata_file,
            "wb"
        ) as f:
            pickle.dump(
                metadata,
                f
            )

    def load(self):
        index = faiss.read_index(
            str(self.index_file)
        )

        with open(
            self.metadata_file,
            "rb"
        ) as f:
            metadata = pickle.load(f)

        return index, metadata