from fastapi import  HTTPException, APIRouter

from database import empenho_collection

from models import (
    SubelementoEmpenhadoSumCollection,
    SubelementoAnoMesEmpenhadoSumCollection
)

#  Configuração do Router
subelemento = APIRouter()


@subelemento.get(
    "/subelementos/empenhado-sum/",
    response_description="Sum of 'Empenhado' values per Subelemento",
    response_model=SubelementoEmpenhadoSumCollection,
    response_model_by_alias=False,
    tags=["Subelementos"],
)
async def sum_empenhado_per_subelemento():
    """
    Retorna a soma de todos os valores empenhados ('Empenhado') para cada subelemento ('Subelemento').
    """
    try:
        # Definição do pipeline de agregação
        pipeline = [
            {
                "$group": {
                    "_id": "$Subelemento",
                    "total_empenhado": { "$sum": "$Empenhado" }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "subelemento": "$_id",
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
        return SubelementoEmpenhadoSumCollection(subelementos=resultados)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@subelemento.get(
    "/subelementos/empenhado-sum-year-month/",
    response_description="Sum of 'Empenhado' values per Subelemento, Year, and Month",
    response_model=SubelementoAnoMesEmpenhadoSumCollection,
    response_model_by_alias=False,
    tags=["Subelementos"],
)
async def sum_empenhado_per_subelemento_year_month():
    """
    Retorna a soma de todos os valores empenhados ('Empenhado') para cada subelemento ('Subelemento'),
    agrupados por ano e mês.
    """
    try:
        # Definição do pipeline de agregação
        pipeline = [
            {
                "$group": {
                    "_id": {
                        "subelemento": "$Subelemento",
                        "ano": { "$year": "$Data" },
                        "mes": { "$month": "$Data" }
                    },
                    "total_empenhado": { "$sum": "$Empenhado" }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "subelemento": "$_id.subelemento",
                    "ano": "$_id.ano",
                    "mes": "$_id.mes",
                    "total_empenhado": 1
                }
            },
            {
                "$sort": { "subelemento": 1, "ano": 1, "mes": 1 }  # Ordena por subelemento, ano e mês
            }
        ]

        # Executa a agregação
        cursor = empenho_collection.aggregate(pipeline)
        resultados = await cursor.to_list(length=None)  # Obtém todos os resultados

        # Retorna a resposta formatada
        return SubelementoAnoMesEmpenhadoSumCollection(subelementos=resultados)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))