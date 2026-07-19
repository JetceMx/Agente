# Oracle Cloud Infrastructure (OCI) Deployment Guide

## Prerequisites
- OCI CLI configured
- Docker installed
- Access to OCI Container Registry (OCIR)

## Steps to Deploy

### 1. Build and Tag the Docker Image
```bash
# Build the image
docker build -t agente-calculo .

# Tag for OCIR
docker tag agente-calculo:latest <your-ocir-namespace>/agente-calculo:latest
```

### 2. Push to OCIR
```bash
# Login to OCIR
docker login <your-ocir-registry>

# Push the image
docker push <your-ocir-namespace>/agente-calculo:latest
```

### 3. Deploy to OCI Container Instances
```bash
# Create a container instance using OCI CLI
oci container-instances container-instance create \
    --compartment-id <your-compartment-id> \
    --display-name "agente-calculo" \
    --containers '[{
        "imageUrl": "<your-ocir-namespace>/agente-calculo:latest",
        "environmentVariables": {
            "OPENAI_API_KEY": "<your-openai-api-key>"
        },
        "resourceConfig": {
            "memoryInGBs": 1,
            "ocpus": 1
        }
    }]' \
    --shape "CI.Standard.E4.1" \
    --vnics '[{
        "subnetId": "<your-subnet-id>",
        "assignPublicIp": true
    }]'
```

### 4. Configure Security
- Store OpenAI API key in OCI Vault
- Use IAM policies to restrict access
- Configure security lists to allow traffic on port 8000

### 5. Alternative: Deploy to OCI Compute Instance
```bash
# SSH into your compute instance
ssh -i <your-key> opc@<instance-ip>

# Install Docker
sudo yum install -y docker
sudo systemctl start docker
sudo usermod -aG docker opc

# Pull and run the container
docker pull <your-ocir-namespace>/agente-calculo:latest
docker run -d \
    -p 8000:8000 \
    -e OPENAI_API_KEY=<your-key> \
    --name agente \
    <your-ocir-namespace>/agente-calculo:latest
```

## Verification
After deployment, verify the application is running:
```bash
curl http://<your-public-ip>:8000/api/health
```

Expected response:
```json
{
    "status": "healthy",
    "message": "El agente está funcionando correctamente"
}
```
