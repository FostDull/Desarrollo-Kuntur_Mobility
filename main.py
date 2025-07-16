import os
import uuid
import time
import logging
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configurar FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "API en funcionamiento"}

# Configuración de carpetas
CARPETA_VIDEOS = "./data/videos"
os.makedirs(CARPETA_VIDEOS, exist_ok=True)

# Mostrar información de entorno (debug/log)
bucket_id = os.getenv("B2_BUCKET_ID")
if not bucket_id:
    logger.warning("⚠️ No se encontró B2_BUCKET_ID en el archivo .env.")
else:
    logger.info(f"Usando bucketId: {bucket_id}")
    

@app.post("/upload-video/")
async def upload_video(file: UploadFile = File(...)):
    # Aceptar múltiples tipos de video
    valid_types = [
        "video/webm",
        "video/mp4",
        "video/quicktime",  # .mov
        "video/x-msvideo",  # .avi
        "application/octet-stream"  # genérico
    ]

    if file.content_type not in valid_types:
        # Verificar por extensión si el tipo MIME falla
        filename = file.filename.lower()
        if not any(filename.endswith(ext) for ext in ['.webm', '.mp4', '.mov', '.avi']):
            raise HTTPException(400, "Tipo de archivo no soportado. Formatos aceptados: .webm, .mp4, .mov, .avi")

    # Generar nombre único
    file_ext = os.path.splitext(file.filename)[1] or ".webm"
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(CARPETA_VIDEOS, unique_filename)

    try:
        start_time = time.time()

        # Guardar el archivo
        with open(file_path, "wb") as f:
            while content := await file.read(1024 * 1024):  # Leer en chunks de 1MB
                f.write(content)

        file_size = os.path.getsize(file_path)
        elapsed = time.time() - start_time

        logger.info(f"📥 Video guardado: {unique_filename} ({file_size / 1024:.1f} KB en {elapsed:.2f}s)")

        return {
            "message": f"Video guardado correctamente",
            "file_name": unique_filename,
            "file_size": file_size
        }

    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        logger.error(f"❌ Error al guardar el video: {str(e)}")
        raise HTTPException(500, f"Error al guardar el video: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
