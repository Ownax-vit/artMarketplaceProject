from uuid import UUID, uuid4

from pydantic import BaseModel, AnyUrl
from pydantic import Field


class Base(BaseModel):
    id: UUID = Field(default_factory=uuid4)

    class Config:
        from_attributes = True


class BaseNaming(BaseModel):
    name: str = Field(..., min_length=5, max_length=255)
    slug_name: str = Field(..., min_length=5, max_length=255)


class BaseCategory(BaseModel):
    url_image: AnyUrl = Field(..., max_length=255)
