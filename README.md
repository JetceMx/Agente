# M.A.R.V.I.N. // Fan Intel

**M.A.R.V.I.N.** significa **Módulo de Asistencia y Respuesta Virtual para
Información de Negocios**. Es un agente de consulta para una comunidad de fans de
Apex Legends y Titanfall, inspirado en los robots MRVN de ese universo.

El proyecto usa un flujo RAG real con **LangChain + Cohere**: divide varios PDFs
en fragmentos, crea embeddings multilingües, recupera la información más relevante
y genera una respuesta indicando el archivo y la página utilizados.

> Proyecto creado por fans. No está afiliado con Electronic Arts ni Respawn
> Entertainment.

## Capacidades

- Consulta simultánea de varios archivos PDF.
- Recuperación semántica con `CohereEmbeddings`.
- Respuestas con `ChatCohere` y Command A.
- Fuentes por nombre de archivo y número de página.
- Memoria breve de conversación.
- Detección de cambios en la biblioteca durante la ejecución.
- Interfaz responsive estilo terminal sci-fi.

## Arquitectura

```text
Navegador
   │
   ▼
FastAPI ──► LangChain
               │
               ├──► PDFs ──► fragmentos ──► Cohere Embeddings
               │                              │
               │                              ▼
               │                       búsqueda semántica
               │                              │
               └──► ChatCohere ◄── contexto recuperado
```

## Biblioteca de documentos

Los documentos deben guardarse dentro de:

```text
pdfs/
├── Apex Legends.pdf
├── Armas.pdf
├── Respawn Entertainment.pdf
├── Titanfall.pdf
└── Titanfall 2.pdf
```

M.A.R.V.I.N. carga automáticamente todos los archivos `*.pdf` de esa carpeta. Si
se agrega, elimina o modifica un archivo, el índice se reconstruye en la siguiente
consulta. Durante la migración, también puede detectar PDFs ubicados en la raíz
cuando `pdfs/` todavía no existe o está vacía.

## Configuración

1. Copia el archivo de ejemplo:

   ```bash
   cp .env.example .env
   ```

2. Agrega tu API key de Cohere:

   ```dotenv
   COHERE_API_KEY=tu-api-key-aqui
   MODEL_NAME=command-a-03-2025
   EMBEDDING_MODEL=embed-multilingual-v3.0
   PDF_DIR=pdfs
   ```

## Ejecución local

Requiere Python 3.11 o superior.

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate

pip install -r requirements.txt
python -m app.main
```

Abre `http://localhost:8000`.

## Ejecución con Docker

```bash
docker compose up --build
```

El directorio local `pdfs/` se monta en modo lectura dentro del contenedor.

## API

| Método | Ruta | Descripción |
|---|---|---|
| `POST` | `/api/ask` | Responde una consulta con fuentes |
| `GET` | `/api/documents` | Lista la biblioteca disponible |
| `POST` | `/api/reset` | Limpia la memoria de conversación |
| `GET` | `/api/health` | Informa estado, modelo y cantidad de PDFs |

Ejemplo:

```bash
curl -X POST http://localhost:8000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"¿Cómo se relacionan Titanfall y Apex Legends?"}'
```

## Pruebas

```bash
python -m unittest -v test_cohere_integration.py
```

Las pruebas usan dobles locales y no envían los PDFs a Cohere.

## Estructura principal

```text
app/
├── api/routes.py
├── core/config.py
├── services/agent.py
├── services/pdf_processor.py
└── main.py
pdfs/
static/
templates/
```
