# app/embeddings_subelementos.py
from langchain_openai.embeddings import OpenAIEmbeddings
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

def get_embedding_model():
    # Inicializar o modelo de embeddings do OpenAI com a chave de API
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    return OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
