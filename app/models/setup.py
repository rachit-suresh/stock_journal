from pydantic import BaseModel
from app.models.common import MongoBaseModel
from typing import Optional


class SetupBase(MongoBaseModel):
    user_id: str  # Placeholder for auth
    name: str
    notes: Optional[str] = None


class SetupCreate(BaseModel):
    name: str
    notes: Optional[str] = None


class SetupDB(SetupBase):
    pass


class SetupOut(SetupBase):
    pass
