from pypdf import PdfReader
import numpy as np
import google.generativeai as genai
from app.core.config import settings


class DocumentProcessor:
    def __init__(self):
        genai.configure(api_key=settings.google_api_key)
        self.chunks = []
        self.embeddings = []

    def load_pdf(self, pdf_path: str) -> str:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text

    def split_text(self, text: str) -> list:
        chunk_size = settings.chunk_size
        chunk_overlap = settings.chunk_overlap
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start = end - chunk_overlap
        return chunks

    def get_embeddings(self, chunks: list) -> list:
        embeddings = []
        for chunk in chunks:
            result = genai.embed_content(
                model="models/text-embedding-004",
                content=chunk
            )
            embeddings.append(result["embedding"])
        return embeddings

    def process_document(self, pdf_path: str = None):
        if pdf_path is None:
            pdf_path = settings.pdf_path
        text = self.load_pdf(pdf_path)
        self.chunks = self.split_text(text)
        self.embeddings = self.get_embeddings(self.chunks)

    def cosine_similarity(self, a, b):
        a = np.array(a)
        b = np.array(b)
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def similarity_search(self, query: str, k: int = 4) -> list:
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=query
        )
        query_embedding = result["embedding"]
        similarities = []
        for i, emb in enumerate(self.embeddings):
            sim = self.cosine_similarity(query_embedding, emb)
            similarities.append((sim, i))
        similarities.sort(reverse=True, key=lambda x: x[0])
        return [self.chunks[idx] for sim, idx in similarities[:k]]


document_processor = DocumentProcessor()
