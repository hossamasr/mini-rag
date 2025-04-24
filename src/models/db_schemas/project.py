from bson.objectid import ObjectId
from typing import Optional
ffrom pydantic import BaseModel, Field, field_validator


class Project(BaseModel):
    id: Optional[ObjectId] = Field(None, alias='_id')  # mongo return Bson
    project_id: str = Field(..., min_length=1)

    @field_validator('project_id')
    def validate_projectid(cls, value):
        if not value.isalnum():
            raise ValueError("proj id must be alphanumeric")

        return value

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def get_indexes(cls):
        return [
            {
                "key": [
                    ("project_id", 1)
                ],
                "name": "project_id_index_1",
                "unique": True
            }
        ]
