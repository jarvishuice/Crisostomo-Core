from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class AuthorEntity(BaseModel):
    cod: Optional[str] = Field(None, description="Código único del autor")
    name: str = Field(..., description="Nombre del autor")
    description: Optional[str] = Field(None, description="Breve descripción del autor")
    created_at: Optional[datetime] = Field(None, description="Fecha de creación")
    updated_at: Optional[datetime] = Field(None, description="Fecha de actualización")

    def serialize(self) -> dict:

        data = self.model_dump()
        if self.created_at:
            data["created_at"] = self.created_at.isoformat()
        if self.updated_at:
            data["updated_at"] = self.updated_at.isoformat()
        if self.cod:
            data["cod"] = self.cod
        if self.description:
            data["description"] = self.description
        return data
