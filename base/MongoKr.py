import os
import logging
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configura logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Leer URI y nombres de DB/colección
uri = os.getenv("MONGO_URI")
db_name = os.getenv("MONGO_DB")
collection_name = os.getenv("MONGO_COLLECTION")

# Usar la forma funcional de conexión
try:
    client = MongoClient(uri, server_api=ServerApi('1'))
    client.admin.command('ping')
    logger.info("✅ Conectado correctamente a MongoDB Atlas")
except Exception as e:
    logger.error(f"❌ Error al conectar a MongoDB: {e}")
    client = None

# Obtener colección si hay conexión
if client:
    db = client[db_name]
    collection = db[collection_name]
else:
    collection = None

# Función para guardar
def guardar_evidencia(data: dict):
    if collection is None:
        logger.warning("⚠️ No hay conexión activa a MongoDB.")
        return

    url = data.get("url_evidencia")
    if not url:
        logger.warning("⚠️ No se encontró URL de evidencia, no se guardó en Mongo.")
        return

    if collection.find_one({"url_evidencia": url}):
        logger.info(f"🔁 Ya existe evidencia con URL: {url}, no se insertó.")
    else:
        try:
            collection.insert_one(data)
            logger.info(f"✅ Evidencia guardada en MongoDB: {url}")
        except Exception as e:
            logger.error(f"❌ Error guardando evidencia: {e}")
