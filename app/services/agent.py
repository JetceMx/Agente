import google.generativeai as genai
from app.core.config import settings
from app.services.pdf_processor import document_processor


class AgentService:
    def __init__(self):
        genai.configure(api_key=settings.google_api_key)
        self.model = genai.GenerativeModel(settings.model_name)
        self.chat = self.model.start_chat(history=[])
        self._initialized = False

    def _initialize(self):
        if not self._initialized:
            document_processor.process_document()
            self._initialized = True

    def ask(self, question: str) -> dict:
        self._initialize()
        relevant_chunks = document_processor.similarity_search(question, k=4)
        context = "\n\n".join(relevant_chunks)

        prompt = f"""Eres un asistente experto de Santo Pegasus Soluciones. Eres un asistente de la Guía Oficial de Ingeniería Back-end.

Usa el siguiente contexto para responder las preguntas de manera clara y detallada. Si la respuesta no se encuentra en el contexto proporcionado, indica que no tienes esa información específica en la guía.

Contexto de la guía:
{context}

Pregunta: {question}

Respuesta:"""

        response = self.chat.send_message(prompt)
        return {
            "answer": response.text,
            "sources": [
                {"content": chunk[:200] + "...", "metadata": {"source": "Lectura.pdf"}}
                for chunk in relevant_chunks
            ]
        }

    def reset_memory(self):
        self.chat = self.model.start_chat(history=[])


agent_service = AgentService()
