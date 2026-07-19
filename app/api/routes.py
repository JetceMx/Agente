from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette.concurrency import run_in_threadpool

from app.core.config import settings
from app.services.agent import agent_service


router = APIRouter()


class QuestionRequest(BaseModel):
    question: str


class SourceResponse(BaseModel):
    content: str
    metadata: dict


class AnswerResponse(BaseModel):
    answer: str
    sources: List[SourceResponse]


class DocumentResponse(BaseModel):
    name: str
    size: int


class CatalogResponse(BaseModel):
    count: int
    documents: List[DocumentResponse]
    indexed: bool
    model: str


def _upstream_status(error: Exception):
    current = error
    visited = set()
    while current is not None and id(current) not in visited:
        visited.add(id(current))
        status = getattr(current, "status_code", None)
        if status:
            return status
        current = current.__cause__ or current.__context__
    return None


@router.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="La pregunta no puede estar vacía.")

    try:
        result = await run_in_threadpool(agent_service.ask, question)
        return AnswerResponse(
            answer=result["answer"],
            sources=[
                SourceResponse(content=source["content"], metadata=source["metadata"])
                for source in result["sources"]
            ],
        )
    except FileNotFoundError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    except Exception as error:
        upstream_status = _upstream_status(error)

        if upstream_status == 404:
            detail = (
                f"El modelo de IA '{settings.model_name}' no está disponible. "
                "Revisa la variable MODEL_NAME."
            )
        elif upstream_status in (401, 403):
            detail = "La API key de Cohere no es válida o no tiene acceso al modelo."
        elif upstream_status == 429:
            detail = "Se alcanzó el límite de solicitudes de Cohere. Intenta más tarde."
        else:
            detail = "M.A.R.V.I.N. no pudo procesar la consulta en este momento."

        raise HTTPException(
            status_code=502 if upstream_status else 500,
            detail=detail,
        ) from error


@router.get("/documents", response_model=CatalogResponse)
async def list_documents():
    return CatalogResponse(**agent_service.catalog())


@router.post("/reset")
async def reset_conversation():
    agent_service.reset_memory()
    return {"message": "Memoria de conversación reiniciada."}


@router.get("/health")
async def health_check():
    catalog = agent_service.catalog()
    return {
        "status": "healthy",
        "agent": "M.A.R.V.I.N.",
        "model": settings.model_name,
        "documents": catalog["count"],
    }
