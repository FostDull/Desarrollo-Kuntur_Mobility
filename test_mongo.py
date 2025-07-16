from pymongo import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://BaseKM:C1kb4PxHDnXu5WGd@cluster1.cmfubru.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1"

try:
    client = MongoClient(uri, server_api=ServerApi("1"))
    client.admin.command("ping")
    print("✅ Conexión exitosa con MongoDB Atlas")
except Exception as e:
    print("❌ Falló la conexión con MongoDB Atlas")
    print(e)
