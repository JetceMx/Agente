# 🤖 Agente Inteligente de Calculo Diferencial

Agente de inteligencia artificial capaz de responder preguntas basadas en el contenido del Capítulo 1: **Precision, Error y Aproximaciones** del libro de Calculo Diferencial.

## 📋 Descripción General

Este proyecto implementa un agente inteligente que utiliza técnicas de Retrieval-Augmented Generation (RAG) para responder preguntas sobre conceptos de precisión, propagación de errores y aproximaciones matemáticas. El agente procesa un documento PDF como fuente de información y utiliza embeddings vectoriales para encontrar y generar respuestas contextuales.

## 🏗️ Arquitectura de la Solución

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (HTML/CSS/JS)                   │
│                     Interfaz de chat intuitiva                   │
└─────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API REST (FastAPI)                         │
│                   Endpoints: /ask, /reset, /health              │
└─────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│              Agente LangChain + Google Gemini                   │
│              ConversationalRetrievalChain                        │
│              + ConversationBufferWindowMemory                    │
└─────────────────────────────────────────────────────────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    ▼                           ▼
┌──────────────────────────┐   ┌──────────────────────────┐
│     ChromaDB             │   │    Google AI Studio       │
│   Vector Store           │   │   Gemini + Embeddings     │
└──────────────────────────┘   └──────────────────────────┘
                    │
                    ▼
┌──────────────────────────┐
│    PDF Processor         │
│   PyPDFLoader            │
└──────────────────────────┘
```

## 🛠️ Tecnologías y Herramientas

| Componente | Tecnología |
|------------|------------|
| **Backend** | Python 3.11, FastAPI |
| **Frontend** | HTML5, CSS3, JavaScript vanilla |
| **IA/ML** | LangChain, Google Gemini 1.5 Flash |
| **Embeddings** | Google text-embedding-004 |
| **Vector Store** | ChromaDB |
| **PDF Processing** | PyPDFLoader |
| **Containerización** | Docker, Docker Compose |
| **Cloud** | Oracle Cloud Infrastructure (OCI) |

## 📁 Estructura del Proyecto

```
agente-calculo-diferencial/
├── app/
│   ├── __init__.py
│   ├── main.py              # Punto de entrada FastAPI
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py        # Configuración del proyecto
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py        # Endpoints de la API
│   └── services/
│       ├── __init__.py
│       ├── pdf_processor.py  # Procesamiento de PDF
│       └── agent.py          # Lógica del agente IA
├── static/
│   ├── styles.css           # Estilos CSS
│   └── script.js            # JavaScript del frontend
├── templates/
│   └── index.html           # Plantilla HTML principal
├── tests/                   # Pruebas unitarias
├── Lectura.pdf              # Documento fuente (Cap 1)
├── requirements.txt         # Dependencias Python
├── Dockerfile               # Configuración Docker
├── docker-compose.yml       # Orquestación Docker
├── .env.example             # Variables de entorno (ejemplo)
├── .gitignore               # Archivos ignorados por Git
└── OCI_DEPLOY.md            # Guía de despliegue en OCI
```

## 🚀 Instrucciones para Ejecutar el Proyecto

### Prerrequisitos
- Python 3.11 o superior
- API Key de Google AI Studio (GRATIS)
- Docker (opcional)

### Obtener API Key Gratuita de Google AI Studio

1. Ve a [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Inicia sesión con tu cuenta de Google
3. Haz clic en "Create API Key"
4. Copia la API Key generada

### Instalación Local

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/tu-usuario/agente-calculo-diferencial.git
   cd agente-calculo-diferencial
   ```

2. **Crear entorno virtual:**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno:**
   ```bash
   # Copiar el archivo de ejemplo
   cp .env.example .env
   
   # Editar .env y agregar tu API key de Google AI Studio
   GOOGLE_API_KEY=tu-api-key-aqui
   ```

5. **Ejecutar la aplicación:**
   ```bash
   python -m app.main
   ```

6. **Abrir el navegador:**
   ```
   http://localhost:8000
   ```

### Con Docker

1. **Construir y ejecutar:**
   ```bash
   docker-compose up --build
   ```

2. **Acceder a la aplicación:**
   ```
   http://localhost:8000
   ```

## 💬 Ejemplos de Preguntas que el Agente Puede Responder

### Sobre Error Absoluto
- "¿Qué es el error absoluto?"
- "¿Cómo se calcula el error absoluto?"
- "Dame la fórmula del error absoluto"

### Sobre Error Relativo
- "¿Qué diferencia hay entre error absoluto y error relativo?"
- "¿Cómo se expresa el error relativo?"
- "¿Qué es el error porcentual?"

### Sobre Propagación de Errores
- "Explica la propagación de errores en sumas"
- "¿Cómo se propagan los errores en multiplicaciones?"
- "¿Qué es la regla de propagation of errors?"

### Sobre Aproximaciones
- "¿Qué son las aproximaciones numéricas?"
- "¿Cómo funciona el método de Newton para aproximar raíces?"
- "¿Qué es una serie de Taylor?"

### Conceptos Generales
- "¿Qué diferencia hay entre precisión y exactitud?"
- "¿Qué es un dígito significativo?"
- "¿Cómo se redondean números con error?"

## 📝 Ejemplos de Respuestas Generadas

**Pregunta:** "¿Qué es el error absoluto?"

**Respuesta del Agente:**
> El error absoluto es la diferencia entre el valor medido o aproximado (x*) y el valor verdadero o exacto (x) de una cantidad. Matemáticamente se expresa como:
>
> **Error Absoluto = |x* - x|**
>
> Donde:
> - x* es el valor aproximado o medido
> - x es el valor verdadero
> - Las barras indican valor absoluto
>
> El error absoluto nos indica cuán lejos está nuestra aproximación del valor real, pero no nos dice qué tan significativo es ese error en relación con la magnitud del valor.

---

**Pregunta:** "¿Cómo se calcula el error relativo?"

**Respuesta del Agente:**
> El error relativo se calcula dividiendo el error absoluto entre el valor verdadero:
>
> **Error Relativo = |x* - x| / |x|**
>
> O expresado como porcentaje:
>
> **Error Porcentual = (|x* - x| / |x|) × 100%**
>
> Ventajas del error relativo:
> 1. Es adimensional (no tiene unidades)
> 2. Proporciona una medida de la precisión relativa
> 3. Permite comparar errores entre mediciones de diferentes magnitudes
>
> Por ejemplo, un error de 1 cm es significativo si mides una pulsera, pero insignificante si mides la distancia entre ciudades.

## ☁️ Evidencia del Deploy en OCI

### Enlace de la Aplicación Desplegada
[https://<tu-endpoint>.oci.oraclecloud.com](https://tu-endpoint.oci.oraclecloud.com)

### Capturas de Pantalla

**Interfaz del Chat:**
![Chat Interface](docs/screenshots/chat-interface.png)

**Respuesta del Agente:**
![Agent Response](docs/screenshots/agent-response.png)

### Verificación del Deploy
```bash
# Verificar que el servicio está activo
curl https://<tu-endpoint>.oci.oraclecloud.com/api/health

# Respuesta esperada
{
    "status": "healthy",
    "message": "El agente está funcionando correctamente"
}
```

## 📌 Notas Importantes

- Google AI Studio ofrece una API **GRATUITA** con límites generosos para desarrollo.
- La primera ejecución procesará el PDF y creará el vector store (puede tomar unos segundos).
- El vector store se persiste en disco para evitar reprocesar el PDF en cada inicio.
- Para reiniciar la conversación, usa el botón "🔄 Nueva Conversación" en la interfaz.

## 📄 Licencia

Este proyecto es para fines educativos.

## 👨‍💻 Autor

[Tu Nombre] - [Tu Email]
