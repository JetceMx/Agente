from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes import router
from app.core.config import settings


app = FastAPI(
    title="M.A.R.V.I.N. Fan Intel",
    description=(
        "Módulo de Asistencia y Respuesta Virtual para una comunidad de fans "
        "de Apex Legends y Titanfall."
    ),
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router, prefix="/api")


@app.get("/", response_class=HTMLResponse)
async def root():
    return HTMLResponse(
        content=Path("templates/index.html").read_text(encoding="utf-8")
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
    )
