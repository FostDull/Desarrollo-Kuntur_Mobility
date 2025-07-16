📹 FastAPI Video Upload API
Una API desarrollada con FastAPI que permite subir archivos de video de forma segura y eficiente. Los archivos se almacenan localmente y se valida su tipo MIME o extensión. Ideal para integrarse con sistemas de almacenamiento como Backblaze B2 o flujos de procesamiento multimedia.

🚀 Características
Subida de videos en formatos .webm, .mp4, .mov, .avi.

Validación de tipo MIME y extensiones.

Logging detallado del proceso de carga.

Soporte para CORS (peticiones desde cualquier origen).

Configuración de entorno mediante .env.

📂 Estructura de Carpetas
kotlin
Copiar
Editar
📁 data/
└── 📁 videos/   ← Carpeta donde se guardan los videos subidos
📦 Requisitos
Python 3.10 o superior

FastAPI

Uvicorn

python-dotenv

Instalación de dependencias:

bash
Copiar
Editar
pip install -r requirements.txt
Ejemplo de requirements.txt:

txt
Copiar
Editar
fastapi
uvicorn
python-dotenv
⚙️ Variables de Entorno
Crear un archivo .env en la raíz del proyecto con el siguiente contenido:

env
Copiar
Editar
B2_BUCKET_ID=tu_bucket_id  # Opcional, para logging o integración futura
🧪 Endpoints
GET /
Verifica que la API esté en funcionamiento:

json
Copiar
Editar
{
  "message": "API en funcionamiento"
}
POST /upload-video/
Sube un archivo de video.

Parámetros:
file: archivo de video (form-data)

Formatos soportados:
.webm, .mp4, .mov, .avi

Ejemplo con curl:
bash
Copiar
Editar
curl -X POST "http://localhost:8001/upload-video/" \
  -H  "accept: application/json" \
  -H  "Content-Type: multipart/form-data" \
  -F "file=@video.mp4"
Respuesta:
json
Copiar
Editar
{
  "message": "Video guardado correctamente",
  "file_name": "e4a3b2f9-73b7-4f5e-b32b-02b929b5b2fa.mp4",
  "file_size": 1048576
}
🖥️ Ejecución local
bash
Copiar
Editar
uvicorn main:app --reload --port 8001
🛡️ Notas de Seguridad
Esta API permite subir archivos desde cualquier origen (CORS). En producción, se recomienda limitar los orígenes permitidos.

Actualmente los archivos se guardan en disco. Para almacenamiento persistente, puede integrarse con servicios como Backblaze B2, Amazon S3, etc.

🎥 Procesamiento Automático de Videos con Watchdog, FastAPI y Backblaze B2
Este proyecto implementa un sistema automático que:

Monitorea una carpeta para detectar nuevos videos.

Procesa el contenido del video.

Genera y guarda resultados en JSON.

Sube evidencia a Backblaze B2 si se detectan alertas.

Extrae y transcribe el audio cuando es necesario.

🧠 Tecnologías Usadas
Python 3.10+

watchdog – para monitoreo en tiempo real.

FastAPI – para endpoints REST (ver otro archivo main.py).

Backblaze B2 – para almacenamiento en la nube.

python-dotenv – para cargar variables de entorno.

Logging y manejo robusto de errores.

Transcripción de audio (asumido desde utils.audio_utils).

📂 Estructura de Carpetas
📁 data/
├── 📁 videos/           ← Carpeta que se monitorea
├── 📁 procesados/       ← Videos procesados y resultados JSON
└── 📁 por_transcribir/  ← Archivos que serán transcritos si tienen alertas

📦 Requisitos
Instala las dependencias necesarias:

bash
Copiar
Editar
pip install -r requirements.txt
Ejemplo de requirements.txt:

txt
Copiar
Editar
watchdog
python-dotenv
También deberías tener las dependencias necesarias en los módulos utils, como:

video_processing.py

backblaze_utils.py

audio_utils.py

⚙️ Configuración .env
Crea un archivo .env en la raíz del proyecto con las siguientes variables:

env
Copiar
Editar
B2_KEY_ID=tu_clave_de_aplicacion
B2_APP_KEY=tu_clave_secreta
B2_BUCKET_ID=tu_bucket_id
🧠 ¿Cómo Funciona?
Se ejecuta el script principal.

Comienza a monitorear la carpeta ./data/videos.

Al detectar un nuevo video (.mp4, .avi, .mov, .webm):

Se espera 2 segundos.

Se analiza el video con procesar_video().

Se guarda el resultado como JSON.

Si hay alertas:

El video se sube a Backblaze B2.

Se mueve a la carpeta de transcripción.

Se extrae y procesa el audio con procesar_audio().

🛠️ Utilidades personalizadas
Estas funciones se importan desde la carpeta utils:

procesar_video(path): analiza el video y devuelve resultados + path del video recortado.

subir_video_b2(path, nombre, key_id, app_key, bucket_id): sube video a Backblaze B2.

procesar_audio(path_video, path_json): extrae y transcribe el audio.

🔊 Procesamiento de Audio y Generación de Reportes Enriquecidos
Este módulo procesa el audio extraído de videos, realiza transcripción con Whisper, genera un resumen y una descripción del delito, y guarda los resultados en MongoDB Atlas. También incorpora geolocalización aproximada usando la IP pública del sistema.

🚀 Características
✅ Extracción automática de audio con FFmpeg

✅ Transcripción usando Whisper (faster-whisper)

✅ Generación de resumen con LLM (generar_resumen)

✅ Generación de descripciones semánticas enriquecidas (generar_descripcion_enriquecida)

✅ Detección de IP pública y ubicación geográfica

✅ Guardado automático en MongoDB Atlas

✅ Limpieza de archivos temporales

🧱 Dependencias
Instala las dependencias necesarias con:

bash
Copiar
Editar
pip install -r requirements.txt
Ejemplo de requirements.txt:

txt
Copiar
Editar
faster-whisper
requests
python-dotenv
También asegúrate de que los siguientes binarios estén disponibles:

ffmpeg

ffprobe

Y los siguientes módulos personalizados existen en utils/:

llm_utils.py → funciones generar_resumen() y generar_descripcion_enriquecida()

base/MongoKr.py → función guardar_evidencia()

🗂️ Entradas y Salidas
📥 Entrada
video_path: Ruta a un video (con o sin audio)

visual_json_path: JSON generado por el análisis visual del video (detecta eventos, objetos, etc.)

📤 Salida
Archivo JSON enriquecido (ejemplo: video123_final.json) con:

Transcripción de audio

Resumen del audio

Descripción enriquecida del evento

Ubicación basada en IP

Datos visuales originales

URL pública (usada en Backblaze)

Los resultados también se guardan automáticamente en MongoDB Atlas.

🧪 Ejemplo de uso
python
Copiar
Editar
from audio_processor import procesar_audio

procesar_audio(
    "./data/por_transcribir/video123.mp4",
    "./data/procesados/video123.json"
)
📄 Ejemplo de salida (*_final.json)
json
Copiar
Editar
{
  "descripcion_delito": "Una persona fue detectada lanzando objetos en la calle...",
  "url_evidencia": "https://f000.backblazeb2.com/file/videoKr/video123.mp4",
  "ip_camara": "192.168.100.249",
  "ubicacion_ip": {
    "ciudad": "Quito",
    "pais": "Ecuador",
    "latitud": -0.2295,
    "longitud": -78.5243
  },
  "analisis_visual": {
    "tipo_evento": "Lanzamiento de objetos",
    "confianza": 0.87,
    "frame_detectado": 194
  },
  "resumen_audio": "El audio indica sonidos de discusión y gritos antes del incidente."
}

