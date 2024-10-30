# app/routes.py
from fastapi import APIRouter, HTTPException
from models_embeddings.models_subelementos import ConsultaRequest, ConsultaResponse
from database_pinecone import vector_store
from langchain_openai import OpenAI
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente para o OpenAI
load_dotenv()
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

embeddings_subelemento = APIRouter()

# Configurar o LLM para geração de resposta
llm = OpenAI(model="gpt-3.5-turbo-instruct",temperature=0.2)

SECRET_KEY = os.getenv("SECRET_KEY")

@embeddings_subelemento.post("/consulta", response_model=ConsultaResponse, tags=["Embeddings"])
def consulta_pinecone_api(request: ConsultaRequest):
    query = request.query
    secret = request.secret
    if secret != SECRET_KEY:
        raise HTTPException(status_code=401, detail="Secret key inválida.")
    try:
        # Realizar a busca no Pinecone com base na query
        retrieved_docs = vector_store.similarity_search(query, k=4)  # Recuperar os 4 mais relevantes
        print("Documentos recuperados com sucesso.")

        # Exibir os documentos recuperados (opcional para logs)
        for doc in retrieved_docs:
            print(f"Documento: {doc.page_content}")

        # Criar um contexto a partir dos documentos recuperados
        context = "\n".join([doc.page_content for doc in retrieved_docs])
        
        # Gerar a resposta usando o modelo LLM
        prompt = f"Com base nestes documentos:\n{context}\n\nPergunta: {query}\nResposta citando subelemento completo:"
        response = llm.invoke(prompt)

        print("Resposta gerada pelo LLM:")
        print(response)
        return ConsultaResponse(resposta=response)

    except Exception as e:
        print(f"Erro durante a busca ou geração de resposta: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar a consulta.")
