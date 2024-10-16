import os
from dotenv import load_dotenv
from typing import Optional, List, Any

from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response
from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator

from typing_extensions import Annotated

from bson import ObjectId
import motor.motor_asyncio
from pymongo import ReturnDocument


load_dotenv()

app = FastAPI(
    title="API - ControlGov - Câmara Municipal de Pinhão/SE",
    summary="A sample application showing how to use FastAPI to add a ReST API to a MongoDB collection.",
)
client: motor.motor_asyncio.AsyncIOMotorClient = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.get_database("CMP")
empenho_collection = db.get_collection("EMPENHOS_DETALHADOS_STAGE")

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]


class EmpenhoModel(BaseModel):
    """
    Container for a single empenho record.
    """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    Número: str = Field(...)
    Data: str = Field(...)
    Credor: str = Field(...)
    Alteração: str = Field(...)
    Empenhado: str = Field(...)
    Liquidado: str = Field(...)
    Pago: str = Field(...)
    Atualizado: str = Field(...)
    link_Detalhes: str = Field(...)
    Poder: str = Field(...)
    Função: str = Field(...)
    Elemento_de_Despesa: str = Field(..., alias="Elemento de Despesa")
    Unid_Administradora: str = Field(..., alias="Unid. Administradora")
    Subfunção: str = Field(...)
    Subelemento: str = Field(...)
    Unid_Orçamentária: str = Field(..., alias="Unid. Orçamentária")
    Fonte_de_recurso: str = Field(..., alias="Fonte de recurso")
    Projeto_Atividade: str = Field(..., alias="Projeto/Atividade")
    Categorias_de_base_legal: str = Field(..., alias="Categorias de base legal")
    Histórico: str = Field(...)
    Itens: List[Any] = Field(..., alias="Item(ns)")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "Número": "8230001",
                "Data": "23/08/2024",
                "Credor": "***.040.305-** - EDSON GIL DOS SANTOS",
                "Alteração": "R$ 0,00",
                "Empenhado": "R$ 300,00",
                "Liquidado": "R$ 300,00",
                "Pago": "R$ 300,00",
                "Atualizado": "23/08/2024",
                "link_Detalhes": "https://portal.sitesagapesistemas.com.br/agape2/portal/ext/despesa/?alias=cmpinhao&p=iDespesa&base=670&tipo=empenho&ano=2024&i=107&a=detalhes",
                "Poder": "1 - LEGISLATIVO",
                "Função": "01 - LEGISLATIVA",
                "Elemento de Despesa": "3390140000 - DIARIAS - CIVIL",
                "Unid. Administradora": "1 - CÂMARA MUNICIPAL DE PINHÃO",
                "Subfunção": "031 - ACAO LEGISLATIVA",
                "Subelemento": "01 - DIARIAS  DENTRO DO ESTADO",
                "Unid. Orçamentária": "10100 - CÂMARA MUNICIPAL DE PINHÃO",
                "Fonte de recurso": "15000000 - Recursos não Vinculados de Impostos",
                "Projeto/Atividade": "2001 - MANUTENÇÃO DAS ATIVIDADES DA CÂMARA MUNICIPAL",
                "Categorias de base legal": "DISPENSADO/2024",
                "Histórico": "VALOR QUE SE EMPENHA REFERENTE A DESPESA DE UMA DIÁRIA INTERMUNICIPAL PARA O PRESIDENTE DA MESA DIRETORA VIAJAR À SERVIÇO DA CÂMARA DE VEREADORES DE PINHÃO, EM VEÍCULO PARTICULAR, PARA FAZER ORÇAMENTO PARA COMPRA DE EQUIPAMENTOS, NA CIDADE DE FREI PAULO/SE.",
                "Item(ns)": [
                    ["Descrição", "Tipo", "Quantidade", "Valor unitário", "Valor Total"],
                    [["DIÁRIA INTERMUNICIPAL", "DRA", "1", "R$300,00", "R$300,00"]]
                ]
            }
        }


class UpdateEmpenhoModel(BaseModel):
    """
    A set of optional updates to be made to a document in the database.
    """
    Número: Optional[str] = None
    Data: Optional[str] = None
    Credor: Optional[str] = None
    Alteração: Optional[str] = None
    Empenhado: Optional[str] = None
    Liquidado: Optional[str] = None
    Pago: Optional[str] = None
    Atualizado: Optional[str] = None
    link_Detalhes: Optional[str] = None
    Poder: Optional[str] = None
    Função: Optional[str] = None
    Elemento_de_Despesa: Optional[str] = Field(None, alias="Elemento de Despesa")
    Unid_Administradora: Optional[str] = Field(None, alias="Unid. Administradora")
    Subfunção: Optional[str] = None
    Subelemento: Optional[str] = None
    Unid_Orçamentária: Optional[str] = Field(None, alias="Unid. Orçamentária")
    Fonte_de_recurso: Optional[str] = Field(None, alias="Fonte de recurso")
    Projeto_Atividade: Optional[str] = Field(None, alias="Projeto/Atividade")
    Categorias_de_base_legal: Optional[str] = Field(None, alias="Categorias de base legal")
    Histórico: Optional[str] = None
    Itens: Optional[List[Any]] = Field(None, alias="Item(ns)")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "Número": "8230001",
                "Data": "23/08/2024",
                "Credor": "***.040.305-** - EDSON GIL DOS SANTOS",
                "Alteração": "R$ 0,00",
                "Empenhado": "R$ 300,00",
                "Liquidado": "R$ 300,00",
                "Pago": "R$ 300,00",
                "Atualizado": "23/08/2024",
                "link_Detalhes": "https://portal.sitesagapesistemas.com.br/agape2/portal/ext/despesa/?alias=cmpinhao&p=iDespesa&base=670&tipo=empenho&ano=2024&i=107&a=detalhes",
                "Poder": "1 - LEGISLATIVO",
                "Função": "01 - LEGISLATIVA",
                "Elemento de Despesa": "3390140000 - DIARIAS - CIVIL",
                "Unid. Administradora": "1 - CÂMARA MUNICIPAL DE PINHÃO",
                "Subfunção": "031 - ACAO LEGISLATIVA",
                "Subelemento": "01 - DIARIAS  DENTRO DO ESTADO",
                "Unid. Orçamentária": "10100 - CÂMARA MUNICIPAL DE PINHÃO",
                "Fonte de recurso": "15000000 - Recursos não Vinculados de Impostos",
                "Projeto/Atividade": "2001 - MANUTENÇÃO DAS ATIVIDADES DA CÂMARA MUNICIPAL",
                "Categorias de base legal": "DISPENSADO/2024",
                "Histórico": "VALOR QUE SE EMPENHA REFERENTE A DESPESA DE UMA DIÁRIA INTERMUNICIPAL PARA O PRESIDENTE DA MESA DIRETORA VIAJAR À SERVIÇO DA CÂMARA DE VEREADORES DE PINHÃO, EM VEÍCULO PARTICULAR, PARA FAZER ORÇAMENTO PARA COMPRA DE EQUIPAMENTOS, NA CIDADE DE FREI PAULO/SE.",
                "Item(ns)": [
                    ["Descrição", "Tipo", "Quantidade", "Valor unitário", "Valor Total"],
                    [["DIÁRIA INTERMUNICIPAL", "DRA", "1", "R$300,00", "R$300,00"]]
                ]
            }
        }



class EmpenhoCollection(BaseModel):
    """
    A container holding a list of `EmpenhoModel` instances.

    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    empenhos: List[EmpenhoModel]


@app.post(
    "/empenhos/",
    response_description="Add new empenho",
    response_model=EmpenhoModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
    tags=["Empenhos"],
)
async def create_empenho(empenho: EmpenhoModel = Body(...)):
    """
    Insert a new empenho record.

    A unique `id` will be created and provided in the response.
    """
    new_empenho = await empenho_collection.insert_one(
        empenho.model_dump(by_alias=True, exclude={"id"})
    )
    created_empenho = await empenho_collection.find_one(
        {"_id": new_empenho.inserted_id}
    )
    return created_empenho


@app.get(
    "/empenhos/",
    response_description="List all empenhos",
    response_model=EmpenhoCollection,
    response_model_by_alias=False,
    tags=["Empenhos"],
)
async def list_empenhos():
    """
    List all of the empenho data in the database.

    The response is unpaginated and limited to 1000 results.
    """
    return EmpenhoCollection(empenhos=await empenho_collection.find().to_list(1000))


@app.get(
    "/empenhos/{id}",
    response_description="Get a single empenho",
    response_model=EmpenhoModel,
    response_model_by_alias=False,
    tags=["Empenhos"],
)
async def show_empenho(id: str):
    """
    Get the record for a specific empenho, looked up by `id`.
    """
    if (
        empenho := await empenho_collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        return empenho

    raise HTTPException(status_code=404, detail=f"Empenho {id} not found")


@app.put(
    "/empenhos/{id}",
    response_description="Update a empenho",
    response_model=EmpenhoModel,
    response_model_by_alias=False,
    tags=["Empenhos"],
)
async def update_empenho(id: str, empenho: UpdateEmpenhoModel = Body(...)):
    """
    Update individual fields of an existing empenho record.

    Only the provided fields will be updated.
    Any missing or `null` fields will be ignored.
    """
    empenho_dict = {
        k: v for k, v in empenho.model_dump(by_alias=True).items() if v is not None
    }

    if len(empenho_dict) >= 1:
        update_result = await empenho_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": empenho},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"Empenho {id} not found")

    # The update is empty, but we should still return the matching document:
    if (existing_empenho := await empenho_collection.find_one({"_id": id})) is not None:
        return existing_empenho

    raise HTTPException(status_code=404, detail=f"Empenho {id} not found")


@app.delete("/empenhos/{id}", response_description="Delete a empenho",tags=["Empenhos"],)
async def delete_empenho(id: str):
    """
    Remove a single empenho record from the database.
    """
    delete_result = await empenho_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"empenho {id} not found")
