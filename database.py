import os
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from dotenv import load_dotenv
import motor.motor_asyncio


load_dotenv()

# Conexão com o MongoDB Atlas
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])

if client is None:
	raise ValueError("Failed to create a MongoDB client")

# Seleciona o banco de dados e a coleção
db = client["CMP"]

# Coleção de empenhos
empenho_collection_stage = db.get_collection("EMPENHOS_DETALHADOS_STAGE")
empenho_collection = db.get_collection("EMPENHOS_DETALHADOS")

