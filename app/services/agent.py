from threading import Lock

from langchain_cohere import ChatCohere, CohereEmbeddings
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.vectorstores import InMemoryVectorStore

from app.core.config import settings
from app.services.pdf_processor import document_processor


SYSTEM_PROMPT = """Eres M.A.R.V.I.N. (Módulo de Asistencia y Respuesta Virtual
para Información de Negocios), un asistente de consulta creado para una comunidad
de fans de Apex Legends y Titanfall.

Responde usando únicamente el contexto recuperado de la biblioteca de PDFs.
Explica con claridad, distingue los hechos documentados de cualquier inferencia y
no inventes datos. Si la biblioteca no contiene la respuesta, dilo de forma directa
y sugiere qué tipo de documento podría resolver la duda. Responde en español salvo
que el usuario solicite otro idioma. Este es un proyecto de fans y no debes presentarte
como un producto oficial de Electronic Arts ni de Respawn Entertainment."""


class AgentService:
    def __init__(self):
        self.llm = ChatCohere(
            cohere_api_key=settings.cohere_api_key,
            model=settings.model_name,
            temperature=settings.temperature,
            max_tokens=2000,
        )
        self.embeddings = CohereEmbeddings(
            cohere_api_key=settings.cohere_api_key,
            model=settings.embedding_model,
        )
        self.vector_store = None
        self.document_signature = ()
        self.index_lock = Lock()
        self.chat_history = []

    def _ensure_index(self):
        current_signature = document_processor.signature()
        if self.vector_store is not None and current_signature == self.document_signature:
            return

        with self.index_lock:
            current_signature = document_processor.signature()
            if (
                self.vector_store is not None
                and current_signature == self.document_signature
            ):
                return

            documents = document_processor.load_documents()
            vector_store = InMemoryVectorStore(self.embeddings)
            vector_store.add_documents(documents=documents)
            self.vector_store = vector_store
            self.document_signature = current_signature

    @staticmethod
    def _response_text(response) -> str:
        if isinstance(response.content, str):
            return response.content
        return "".join(
            block.get("text", "")
            for block in response.content
            if isinstance(block, dict)
        ).strip()

    def ask(self, question: str) -> dict:
        self._ensure_index()
        relevant_documents = self.vector_store.similarity_search(
            question,
            k=settings.top_k,
        )

        context = "\n\n".join(
            (
                f"[Archivo: {document.metadata['source']} | "
                f"Página: {document.metadata['page']}]\n"
                f"{document.page_content}"
            )
            for document in relevant_documents
        )
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            *self.chat_history,
            HumanMessage(
                content=(
                    "Contexto recuperado de la biblioteca:\n\n"
                    f"{context}\n\n"
                    f"Pregunta del usuario: {question}"
                )
            ),
        ]
        response = self.llm.invoke(messages)
        answer = self._response_text(response)

        self.chat_history.extend(
            [
                HumanMessage(content=question),
                AIMessage(content=answer),
            ]
        )
        self.chat_history = self.chat_history[-settings.history_turns * 2 :]

        sources = []
        seen_sources = set()
        for document in relevant_documents:
            source_key = (
                document.metadata["source"],
                document.metadata["page"],
            )
            if source_key in seen_sources:
                continue
            seen_sources.add(source_key)
            sources.append(
                {
                    "content": document.page_content[:240] + "...",
                    "metadata": {
                        "source": document.metadata["source"],
                        "page": document.metadata["page"],
                    },
                }
            )

        return {
            "answer": answer,
            "sources": sources,
        }

    def reset_memory(self):
        self.chat_history = []

    def catalog(self) -> dict:
        documents = document_processor.catalog()
        return {
            "count": len(documents),
            "documents": documents,
            "indexed": self.vector_store is not None,
            "model": settings.model_name,
        }


agent_service = AgentService()
