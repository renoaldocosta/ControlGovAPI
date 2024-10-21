from fastapi import FastAPI
from routers.empenhos import empenho
from routers.credores import credor

app = FastAPI(
    title="API - ControlGov - Câmara Municipal de Pinhão/SE",
    version="1.0.1",
    summary="Serviço de aplicação para gestão interna e controle de despesas da Câmara Municipal de Pinhão/SE.",
)


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "API - ControlGov - Câmara Municipal de Pinhão/SE"}

app.include_router(credor)
app.include_router(empenho)


