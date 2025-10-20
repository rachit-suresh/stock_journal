from fastapi import APIRouter, Depends, HTTPException, status
from app.db.database import get_setups_collection
from app.models.setup import SetupCreate, SetupOut, SetupDB
from bson import ObjectId
from typing import List

router = APIRouter(prefix="/api/v1/setups", tags=["Setups"])
USER_ID = "static_user_id"  # Placeholder


@router.post("/", response_model=SetupOut, response_model_by_alias=True, status_code=status.HTTP_201_CREATED)
async def create_setup(
    setup: SetupCreate,
    collection=Depends(get_setups_collection)
):
    setup_db = SetupDB(**setup.model_dump(), user_id=USER_ID)
    # Exclude None values to let MongoDB auto-generate _id
    new_setup = await collection.insert_one(setup_db.model_dump(by_alias=True, exclude_none=True))
    created_setup = await collection.find_one({"_id": new_setup.inserted_id})
    return SetupOut.model_validate(created_setup)


@router.get("/", response_model=List[SetupOut], response_model_by_alias=True)
async def get_all_setups(
    collection=Depends(get_setups_collection)
):
    setups = []
    cursor = collection.find({"user_id": USER_ID})
    async for doc in cursor:
        setups.append(SetupOut.model_validate(doc))
    return setups
