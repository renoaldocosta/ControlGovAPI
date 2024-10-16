# C:\SCRIPTS_INFNET\RD5_Projeto\Livro\Teste\database.py

import os
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from dotenv import load_dotenv

load_dotenv()


# Conexão com o MongoDB Atlas
client: AsyncIOMotorClient =AsyncIOMotorClient(os.environ["MONGODB_URL"])

database = client.livro  # Nome do banco de dados

# Coleções
product_collection = database.get_collection("products")

# Função para converter documentos do MongoDB para dicionário com id como string
def product_helper(product) -> dict:
    return {
        "id": str(product["_id"]),
        "name": product["name"],
        "description": product.get("description", ""),
        "price": product["price"],
        "quantity": product["quantity"],
    }
