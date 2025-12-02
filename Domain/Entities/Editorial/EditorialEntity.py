from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class EditorialEntity(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None

    def serialize(self) -> dict:

        data = self.model_dump()
        if self.created_at:
            data["created_at"] = self.created_at.isoformat()
        if self.description:
            data["description"] = self.description.upper()

        return data
