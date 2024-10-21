from fastapi import FastAPI
from routers.empenhos import empenho
from routers.credores import credor
import requests

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


def obter_ip(formato: str):
    """Obtém o IP no formato especificado ('ipv4' ou 'ipv6')."""
    try:
        if formato == "ipv4":
            resposta = requests.get("https://api.my-ip.io/ip.json")
        elif formato == "ipv6":
            resposta = requests.get("https://api64.ipify.org?format=json")

        resposta.raise_for_status()
        return resposta.json().get("ip")
    except requests.exceptions.RequestException as e:
        return None  # Retorna None se não for possível obter o IP

@app.get("/ip")
def mostrar_ip():
    ipv4 = obter_ip("ipv4")
    ipv6 = obter_ip("ipv6")

    if not ipv4 and not ipv6:
        raise HTTPException(status_code=500, detail="Não foi possível obter nenhum IP.")

    # Prioriza IPv4, mas inclui IPv6 se disponível
    return {
        "ip_publico_ipv4": ipv4 or "Não disponível",
        "ip_publico_ipv6": ipv6 or "Não disponível"
    }
