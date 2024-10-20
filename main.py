from fastapi import FastAPI
from routers.empenhos import empenho

app = FastAPI(
    title="API - ControlGov - Câmara Municipal de Pinhão/SE",
    version="1.0.1",
    summary="Serviço de aplicação para gestão interna e controle de despesas da Câmara Municipal de Pinhão/SE.",
)

app.include_router(empenho)
