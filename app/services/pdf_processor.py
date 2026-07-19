from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

from app.core.config import settings


class DocumentProcessor:
    def __init__(self):
        self.pdf_dir = Path(settings.pdf_dir)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""],
        )

    def list_pdf_files(self) -> list[Path]:
        configured_files = (
            sorted(self.pdf_dir.glob("*.pdf"), key=lambda path: path.name.casefold())
            if self.pdf_dir.is_dir()
            else []
        )
        if configured_files:
            return configured_files

        # Compatibilidad temporal mientras los PDFs existentes se trasladan
        # desde la raíz a la carpeta configurada.
        return sorted(Path(".").glob("*.pdf"), key=lambda path: path.name.casefold())

    def signature(self) -> tuple[tuple[str, int, int], ...]:
        return tuple(
            (str(path.resolve()), path.stat().st_size, path.stat().st_mtime_ns)
            for path in self.list_pdf_files()
        )

    def load_documents(self) -> list[Document]:
        pdf_files = self.list_pdf_files()
        if not pdf_files:
            raise FileNotFoundError(
                f"No se encontraron archivos PDF en la carpeta '{settings.pdf_dir}'."
            )

        pages: list[Document] = []
        for pdf_path in pdf_files:
            reader = PdfReader(str(pdf_path))
            for page_number, page in enumerate(reader.pages, start=1):
                text = (page.extract_text() or "").strip()
                if not text:
                    continue
                pages.append(
                    Document(
                        page_content=text,
                        metadata={
                            "source": pdf_path.name,
                            "page": page_number,
                        },
                    )
                )

        if not pages:
            raise ValueError("Los PDFs disponibles no contienen texto extraíble.")

        chunks = self.text_splitter.split_documents(pages)
        for index, chunk in enumerate(chunks):
            chunk.metadata["chunk"] = index
        return chunks

    def catalog(self) -> list[dict]:
        return [
            {
                "name": path.name,
                "size": path.stat().st_size,
            }
            for path in self.list_pdf_files()
        ]


document_processor = DocumentProcessor()
