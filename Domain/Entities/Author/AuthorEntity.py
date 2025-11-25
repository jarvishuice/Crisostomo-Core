from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime




class AuthorEntity(BaseModel):
    cod: Optional[str] = Field(None, description="Código único del autor")
    name: str = Field(..., description="Nombre del autor")
    description: Optional[str] = Field(None, description="Breve descripción del autor")
    created_at: Optional[datetime] = Field(None, description="Fecha de creación")
    updated_at: Optional[datetime] = Field(None, description="Fecha de actualización")

    class Config:
        from_attributes = True  # para compatibilidad con ORMs si luego se usa


