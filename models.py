# C:\SCRIPTS_INFNET\RD5_Projeto\Livro\Teste\models.py

from pydantic import BaseModel, Field
from typing import Optional

from typing import Optional, List, Any

from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator

from typing_extensions import Annotated

from bson import ObjectId


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
                "Número": "999999999",
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
                "Número": "999999999",
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
