import unittest
from unittest.mock import patch

from fastapi import HTTPException
from langchain_core.documents import Document
from langchain_core.messages import AIMessage

from app.api.routes import QuestionRequest, ask_question
from app.core.config import settings
from app.services.agent import AgentService, SYSTEM_PROMPT
from app.services.pdf_processor import document_processor


class FakeVectorStore:
    def similarity_search(self, question, k):
        return [
            Document(
                page_content="Los Juegos Apex se celebran en los Outlands.",
                metadata={"source": "Apex Legends.pdf", "page": 2},
            ),
            Document(
                page_content="Información adicional sobre los Juegos Apex.",
                metadata={"source": "Apex Legends.pdf", "page": 3},
            ),
        ]


class FakeChatModel:
    def __init__(self):
        self.last_messages = None

    def invoke(self, messages):
        self.last_messages = messages
        return AIMessage(content="Respuesta recuperada por M.A.R.V.I.N.")


class FakeNotFoundError(Exception):
    status_code = 404

    def __str__(self):
        return "headers: {'internal': 'value'}, status_code: 404"


class AgentServiceTests(unittest.TestCase):
    def test_ask_uses_langchain_context_and_returns_sources(self):
        service = AgentService()
        service.vector_store = FakeVectorStore()
        service.llm = FakeChatModel()

        with patch.object(service, "_ensure_index"):
            result = service.ask("¿Qué son los Juegos Apex?")

        self.assertIn("M.A.R.V.I.N.", SYSTEM_PROMPT)
        self.assertEqual(settings.model_name, "command-a-03-2025")
        self.assertEqual(result["answer"], "Respuesta recuperada por M.A.R.V.I.N.")
        self.assertEqual(len(result["sources"]), 2)
        self.assertEqual(result["sources"][0]["metadata"]["page"], 2)
        self.assertIn(
            "Apex Legends.pdf",
            service.llm.last_messages[-1].content,
        )

    def test_document_catalog_finds_all_current_pdfs(self):
        names = [path.name for path in document_processor.list_pdf_files()]

        self.assertEqual(len(names), 5)
        self.assertIn("Apex Legends.pdf", names)
        self.assertIn("Titanfall 2.pdf", names)


class RouteErrorTests(unittest.IsolatedAsyncioTestCase):
    async def test_model_not_found_error_is_sanitized(self):
        with patch(
            "app.api.routes.agent_service.ask",
            side_effect=FakeNotFoundError(),
        ):
            with self.assertRaises(HTTPException) as raised:
                await ask_question(QuestionRequest(question="Pregunta válida"))

        self.assertEqual(raised.exception.status_code, 502)
        self.assertIn("command-a-03-2025", raised.exception.detail)
        self.assertNotIn("headers", raised.exception.detail)
        self.assertNotIn("internal", raised.exception.detail)


if __name__ == "__main__":
    unittest.main()
