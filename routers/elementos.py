from fastapi import  HTTPException, APIRouter

from models import ElementoDespesaEmpenhadoSumCollection, ElementoDespesaAnoMesEmpenhadoSumCollection

from database import empenho_collection


elemento = APIRouter()

@elemento.get(
    "/elementos/despesa/empenhado-sum/",
    response_description="Sum of 'Empenhado' values per Elemento de Despesa",
    response_model=ElementoDespesaEmpenhadoSumCollection,
    response_model_by_alias=False,
    tags=["Elementos de Despesa"],
)
async def sum_empenhado_per_elemento_de_despesa():
    """
    Retorna a soma de todos os valores empenhados ('Empenhado') para cada elemento de despesa ('Elemento de Despesa').
    """
    try:
        # Definição do pipeline de agregação
        pipeline = [
            {
                "$group": {
                    "_id": "$Elemento de Despesa",
                    "total_empenhado": { "$sum": "$Empenhado" }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "elemento_de_despesa": "$_id",
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
        return ElementoDespesaEmpenhadoSumCollection(elementos=resultados)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@elemento.get(
    "/elementos/despesa/empenhado-sum-year-month/",
    response_description="Sum of 'Empenhado' values per Elemento de Despesa, Year, and Month",
    response_model=ElementoDespesaAnoMesEmpenhadoSumCollection,
    response_model_by_alias=False,
    tags=["Elementos de Despesa"],
)
async def sum_empenhado_per_elemento_de_despesa_year_month():
    """
    Retorna a soma de todos os valores empenhados ('Empenhado') para cada elemento de despesa ('Elemento de Despesa'),
    agrupados por ano e mês.
    """
    try:
        # Definição do pipeline de agregação
        pipeline = [
            {
                "$group": {
                    "_id": {
                        "elemento_de_despesa": "$Elemento de Despesa",
                        "ano": { "$year": "$Data" },
                        "mes": { "$month": "$Data" }
                    },
                    "total_empenhado": { "$sum": "$Empenhado" }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "elemento_de_despesa": "$_id.elemento_de_despesa",
                    "ano": "$_id.ano",
                    "mes": "$_id.mes",
                    "total_empenhado": 1
                }
            },
            {
                "$sort": { "elemento_de_despesa": 1, "ano": 1, "mes": 1 }  # Ordena por elemento, ano e mês
            }
        ]

        # Executa a agregação
        cursor = empenho_collection.aggregate(pipeline)
        resultados = await cursor.to_list(length=None)  # Obtém todos os resultados

        # Retorna a resposta formatada
        return ElementoDespesaAnoMesEmpenhadoSumCollection(elementos=resultados)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))