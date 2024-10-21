from fastapi import  HTTPException, APIRouter

from models import CredoresCollection, CredorEmpenhadoSumCollection, CredorEmpenhadoSum

from database import empenho_collection

credor = APIRouter()


@credor.get(
    "/credores/",
    response_description="List all unique credores",
    response_model=CredoresCollection,
    response_model_by_alias=False,
    tags=["Credores"],
)
async def list_credores():
    """
    Retorna uma lista de credores únicos presentes na base de dados.
    """
    try:
        # Utilizando 'distinct' para obter valores únicos do campo 'Credor'
        credores = await empenho_collection.distinct("Credor")
        
        # Opcional: Ordenar a lista de credores
        credores_sorted = sorted(credores)
        
        return CredoresCollection(credores=credores_sorted)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@credor.get(
    "/credores/empenhado-sum/",
    response_description="Sum of 'Empenhado' values per Credor",
    response_model=CredorEmpenhadoSumCollection,
    response_model_by_alias=False,
    tags=["Credores"],
)
async def sum_empenhado_per_credor():
    """
    Retorna a soma de todos os valores empenhados ('Empenhado') para cada credor ('Credor').
    """
    try:
        # Definição do pipeline de agregação simplificado
        pipeline = [
            {
                "$group": {
                    "_id": "$Credor",
                    "total_empenhado": { "$sum": "$Empenhado" }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "credor": "$_id",
                    "total_empenhado": 1
                }
            },
            {
                "$sort": { "total_empenhado": -1 }  # Ordena de forma decrescente
            }
        ]

        # Executa a agregação
        cursor = empenho_collection.aggregate(pipeline)
        resultados = await cursor.to_list(length=None)  # Obtém todos os resultados

        # Retorna a resposta formatada
        return CredorEmpenhadoSumCollection(credores=resultados)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))