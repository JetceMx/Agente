import inspect
import unittest
from unittest.mock import patch

import cohere
from fastapi import HTTPException

from app.api.routes import QuestionRequest, ask_question
from app.core.config import settings
from app.services.agent import AgentService


class FakeChatResponse:
    text = "Respuesta de prueba"


class FakeCohereClient:
    def __init__(self):
        self.last_request = None

    def chat(self, **kwargs):
        self.last_request = kwargs
        return FakeChatResponse()


class FakeNotFoundError(Exception):
    status_code = 404

    def __str__(self):
        return "headers: {'internal': 'value'}, status_code: 404"


class AgentServiceTests(unittest.TestCase):
    def test_sdk_supports_current_chat_contract(self):
        parameters = inspect.signature(cohere.Client.chat).parameters

        for name in (
            "model",
            "message",
            "documents",
            "preamble",
            "temperature",
            "max_tokens",
        ):
            self.assertIn(name, parameters)

    def test_ask_uses_configured_model(self):
        service = AgentService()
        fake_client = FakeCohereClient()
        service.co = fake_client
        service.full_text = "Contenido de prueba del documento."

        result = service.ask("¿Cuál es el tema?")

        self.assertEqual(settings.model_name, "command-a-03-2025")
        self.assertEqual(
            fake_client.last_request["model"],
            "command-a-03-2025",
        )
        self.assertEqual(result["answer"], "Respuesta de prueba")
        self.assertEqual(len(result["sources"]), 1)


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
