from pydantic import BaseModel, Field, ConfigDict
from pydantic.functional_validators import BeforeValidator
from typing import Annotated

# This ensures we can validate strings as ObjectIds
PyObjectId = Annotated[str, BeforeValidator(str)]


class MongoBaseModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        by_alias=True,
    )
    
    id: PyObjectId | None = Field(alias="_id", default=None)
