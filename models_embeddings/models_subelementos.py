# app/models_subelementos.py
from pydantic import BaseModel

class ConsultaRequest(BaseModel):
    query: str
    secret: str

class ConsultaResponse(BaseModel):
    resposta: str
