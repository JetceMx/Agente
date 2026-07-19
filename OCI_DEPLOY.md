# Despliegue de M.A.R.V.I.N. en OCI

## Requisitos

- OCI CLI configurada.
- Docker.
- Acceso a Oracle Cloud Infrastructure Registry (OCIR).
- API key de Cohere almacenada de forma segura.
- Los PDFs dentro de `pdfs/` antes de construir la imagen.

## 1. Construir y etiquetar la imagen

```bash
docker build -t marvin-fan-intel .
docker tag marvin-fan-intel:latest \
  <namespace-ocir>/marvin-fan-intel:latest
```

## 2. Publicar en OCIR

```bash
docker login <registro-ocir>
docker push <namespace-ocir>/marvin-fan-intel:latest
```

## 3. Crear la instancia de contenedor

Configura estas variables en el contenedor:

```text
COHERE_API_KEY=<secreto-desde-oci-vault>
MODEL_NAME=command-a-03-2025
EMBEDDING_MODEL=embed-multilingual-v3.0
PDF_DIR=pdfs
```

Usa la imagen:

```text
<namespace-ocir>/marvin-fan-intel:latest
```

Expón el puerto `8000` y asigna una IP pública o un balanceador según el entorno.

## 4. Seguridad

- Guarda `COHERE_API_KEY` en OCI Vault.
- No copies `.env` dentro de la imagen.
- Restringe el acceso con políticas IAM.
- Habilita únicamente el puerto necesario.
- Trata los PDFs como contenido privado si no son documentos públicos.

## 5. Alternativa en una instancia Compute

```bash
docker pull <namespace-ocir>/marvin-fan-intel:latest

docker run -d \
  -p 8000:8000 \
  -e COHERE_API_KEY=<tu-api-key> \
  -e MODEL_NAME=command-a-03-2025 \
  -e EMBEDDING_MODEL=embed-multilingual-v3.0 \
  -e PDF_DIR=pdfs \
  --name marvin \
  <namespace-ocir>/marvin-fan-intel:latest
```

## Verificación

```bash
curl http://<ip-publica>:8000/api/health
```

Respuesta esperada:

```json
{
  "status": "healthy",
  "agent": "M.A.R.V.I.N.",
  "model": "command-a-03-2025",
  "documents": 5
}
```
