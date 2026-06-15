from pathlib import Path

from pypdf import PdfReader

from src.tools.RAG.chunking import TextChunker
from src.tools.RAG.embeddings import EmbeddingModel
from src.tools.RAG.vector_store import VectorStore


class Ingestor:

    def __init__(self):

        self.documents_path = Path(
            "data/documents"
        )

        self.chunker = TextChunker()
        self.embedding_model = EmbeddingModel()
        self.vector_store = VectorStore()

    def ingest(self):

        metadata = []
        chunk_id = 0

        for pdf_file in self.documents_path.glob("*.pdf"):

            print(f"Processing {pdf_file.name}")

            reader = PdfReader(pdf_file)

            for page_num, page in enumerate(
                reader.pages,
                start=1
            ):

                text = page.extract_text()

                if not text:
                    continue

                chunks = self.chunker.chunk_text(
                    text
                )

                for chunk in chunks:

                    metadata.append(
                        {
                            "id": chunk_id,
                            "source": pdf_file.name,
                            "page": page_num,
                            "text": chunk,
                        }
                    )

                    chunk_id += 1

        print(f"Total Chunks: {len(metadata)}")

        embeddings = self.embedding_model.embed_documents(
            [
                item["text"]
                for item in metadata
            ]
        )

        index = self.vector_store.create_index(
            embeddings.astype("float32")
        )

        self.vector_store.save(
            index=index,
            metadata=metadata
        )

        print("Ingestion Complete")