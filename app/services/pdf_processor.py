from pypdf import PdfReader
from app.core.config import settings


class DocumentProcessor:
    def __init__(self):
        self.full_text = ""

    def load_pdf(self, pdf_path: str) -> str:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text

    def process_document(self, pdf_path: str = None):
        if pdf_path is None:
            pdf_path = settings.pdf_path
        self.full_text = self.load_pdf(pdf_path)

    def get_relevant_text(self, query: str = None, max_chars: int = 8000) -> str:
        if not self.full_text:
            self.process_document()
        return self.full_text[:max_chars]


document_processor = DocumentProcessor()
