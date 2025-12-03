from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class BookEntity(BaseModel):
    code: str
    name: str
    description: Optional[str] = "sin descripción"
    knowledge_area: str
    sub_area: str
    category: str
    editorial_code: str
    uploaded_by: str
    created_at: Optional[datetime] = Field(None, description="Fecha de creación")
    author:str
    process_img: bool = False

    def serialize(self) -> dict:
        data = self.model_dump()
        if self.created_at:
            data["created_at"] = self.created_at.isoformat()

        return data
