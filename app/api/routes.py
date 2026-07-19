from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
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
        raise HTTPException(status_code=500, detail=f"Error al procesar la pregunta: {str(e)}")


@router.post("/reset")
async def reset_conversation():
    agent_service.reset_memory()
    return {"message": "Conversación reiniciada exitosamente"}


@router.get("/health")
async def health_check():
    return {"status": "healthy", "message": "El agente está funcionando correctamente"}
