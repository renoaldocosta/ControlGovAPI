# app/database.py
import os
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore
from embeddings_subelementos import get_embedding_model
from pinecone import Pinecone

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Recuperar as credenciais do Pinecone das variáveis de ambiente
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")  # Exemplo: 'us-east1-gcp'

# Inicializar o cliente Pinecone uma única vez para reutilização
try:
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index_name = "subelementos"
    
    if index_name in [index_info["name"] for index_info in pc.list_indexes()]:
        index = pc.Index(index_name)
        print(f"Conectado ao índice '{index_name}'.")
    else:
        raise Exception(f"Índice '{index_name}' não encontrado.")
except Exception as e:
    print(f"Erro ao conectar ao índice Pinecone: {e}")
    exit()

# Criar o vector store para consulta utilizando o modelo de embeddings
embedding_model = get_embedding_model()
vector_store = PineconeVectorStore(index=index, embedding=embedding_model)
