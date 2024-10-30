# app/models_subelementos.py
from pydantic import BaseModel

class ConsultaRequest(BaseModel):
    query: str
    secret: str
    
    class Config():
        json_schema_extra = {
            "example": {
                "query": "Qual o total empenhado para Fretes?",
                "secret": "my_secret"
            }
        }

class ConsultaResponse(BaseModel):
    resposta: str
