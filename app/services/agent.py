import cohere
from app.core.config import settings


class AgentService:
    def __init__(self):
        self.co = cohere.Client(settings.cohere_api_key)
        self.chat_history = []
        self.full_text = ""

    def _load_document(self):
        from pypdf import PdfReader
        reader = PdfReader(settings.pdf_path)
        self.full_text = ""
        for page in reader.pages:
            self.full_text += page.extract_text() + "\n"

    def ask(self, question: str) -> dict:
        if not self.full_text:
            self._load_document()

        context = self.full_text[:8000]

        response = self.co.chat(
            model=settings.model_name,
            message=question,
            documents=[{"title": "Guia Back-end Santo Pegasus", "snippet": context}],
            preamble="""Eres un asistente experto de Santo Pegasus Soluciones. Responde basándote en la Guía Oficial de Ingeniería Back-end. Si la información no está en la guía, indica que no tienes esa información.""",
            temperature=settings.temperature,
            max_tokens=2000,
        )

        self.chat_history.append({"user": question, "bot": response.text})

        return {
            "answer": response.text,
            "sources": [{"content": context[:200] + "...", "metadata": {"source": "Lectura.pdf"}}]
        }

    def reset_memory(self):
        self.chat_history = []


agent_service = AgentService()
