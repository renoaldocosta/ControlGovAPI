
from fastapi import Body, HTTPException, status, APIRouter
from fastapi.responses import Response

from bson import ObjectId

from models import EmpenhoModel, EmpenhoCollection, UpdateEmpenhoModel

from database import empenho_collection_stage

from pymongo import ReturnDocument

empenho = APIRouter()


@empenho.post(
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
    new_empenho = await empenho_collection_stage.insert_one(
        empenho.model_dump(by_alias=True, exclude={"id"})
    )
    created_empenho = await empenho_collection_stage.find_one(
        {"_id": new_empenho.inserted_id}
    )
    return created_empenho


@empenho.get(
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
    return EmpenhoCollection(empenhos=await empenho_collection_stage.find().to_list(1000))


@empenho.get(
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
        empenho := await empenho_collection_stage.find_one({"_id": ObjectId(id)})
    ) is not None:
        return empenho

    raise HTTPException(status_code=404, detail=f"Empenho {id} not found")


@empenho.put(
    "/empenhos/{id}",
    response_description="Update a empenho",
    response_model=EmpenhoModel,
    response_model_by_alias=False,
    tags=["Empenhos"],
    include_in_schema=False,
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
        update_result = await empenho_collection_stage.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": empenho},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"Empenho {id} not found")

    # The update is empty, but we should still return the matching document:
    if (existing_empenho := await empenho_collection_stage.find_one({"_id": id})) is not None:
        return existing_empenho

    raise HTTPException(status_code=404, detail=f"Empenho {id} not found")


@empenho.delete("/empenhos/{id}", response_description="Delete a empenho",tags=["Empenhos"],include_in_schema=False,)
async def delete_empenho(id: str):
    """
    Remove a single empenho record from the database.
    """
    delete_result = await empenho_collection_stage.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"empenho {id} not found")