from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
import boto3
import os
import httpx
from dotenv import load_dotenv
from urllib.parse import unquote

# Carregar variáveis do ambiente
load_dotenv()

app = FastAPI()

# Configuração do LocalStack
LOCALSTACK_URL = os.getenv("LOCALSTACK_URL", "http://localhost:4566")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# Configurar cliente S3 apontando para o LocalStack
s3_client = boto3.client(
    "s3",
    endpoint_url=LOCALSTACK_URL,
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name=AWS_REGION,
)

# Modelo para requisição de URL pré-assinada
class PresignedUrlRequest(BaseModel):
    fileName: str
    fileType: str

@app.post("/api/generate-presigned-url")
async def generate_presigned_url(request: PresignedUrlRequest):
    try:
        object_name = f"input/{request.fileName}"
        presigned_url = s3_client.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": "files-to-process",
                "Key": object_name,
                "ContentType": request.fileType,
            },
            ExpiresIn=3600,
        )
        return {"presignedUrl": presigned_url}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Could not generate presigned URL")

@app.get("/api/{bucket_name}/list-files")
async def list_files(bucket_name: str):
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix="input/")
        files = []
        if "Contents" in response:
            for obj in response["Contents"]:
                files.append(
                    {
                        "key": obj["Key"],
                        "url": f"{LOCALSTACK_URL}/{bucket_name}/{obj['Key']}",
                    }
                )
        return {"files": files}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Could not list files in S3 bucket")

@app.delete("/api/{bucket_name}/delete-file/{file_key:path}")
async def delete_file(bucket_name: str, file_key: str):
    try:
        decoded_key = unquote(file_key)

        # Verifica se o arquivo existe antes de tentar deletar
        try:
            s3_client.head_object(Bucket=bucket_name, Key=decoded_key)
        except:
            raise HTTPException(status_code=404, detail=f"File {decoded_key} not found in bucket {bucket_name}")

        # Deleta o arquivo
        s3_client.delete_object(Bucket=bucket_name, Key=decoded_key)

        return {"message": f"File {decoded_key} deleted successfully from bucket {bucket_name}"}
    except Exception as e:
        print(f"Error deleting file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Could not delete file: {str(e)}")


@app.put("/api/{bucket_name}/upload-file")
async def upload_file(file: UploadFile = File(...), presigned_url: str = ""):
    try:
        if not presigned_url:
            raise HTTPException(status_code=400, detail="Presigned URL is required")

        # Lê o conteúdo do arquivo de forma assíncrona
        file_content = await file.read()

        # Usando httpx para fazer o upload do arquivo de forma assíncrona
        async with httpx.AsyncClient() as client:
            response = await client.put(presigned_url, content=file_content)

        # Verifica se o upload foi bem-sucedido
        if response.status_code == 200:
            return {"message": "Upload bem-sucedido!"}
        else:
            raise HTTPException(status_code=response.status_code, detail="Falha no upload")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao fazer o upload: {str(e)}")