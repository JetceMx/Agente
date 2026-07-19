from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
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


@router.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="La pregunta no puede estar vacía")

    try:
        result = agent_service.ask(request.question)
        return AnswerResponse(
            answer=result["answer"],
            sources=[
                SourceResponse(content=s["content"], metadata=s["metadata"])
                for s in result["sources"]
            ]
        )
    except Exception as e:
        upstream_status = getattr(e, "status_code", None)

        if upstream_status == 404:
            detail = (
                f"El modelo de IA '{settings.model_name}' no está disponible. "
                "Revisa la variable MODEL_NAME."
            )
        elif upstream_status in (401, 403):
            detail = "La API key de Cohere no es válida o no tiene acceso al modelo configurado."
        elif upstream_status == 429:
            detail = "Se alcanzó el límite de solicitudes de Cohere. Intenta de nuevo más tarde."
        else:
            detail = "No se pudo procesar la pregunta con el servicio de IA."

        raise HTTPException(
            status_code=502 if upstream_status else 500,
            detail=detail,
        ) from e


@router.post("/reset")
async def reset_conversation():
    agent_service.reset_memory()
    return {"message": "Conversación reiniciada exitosamente"}


@router.get("/health")
async def health_check():
    return {"status": "healthy", "message": "El agente está funcionando correctamente"}
