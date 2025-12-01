from pydantic import BaseModel


class CategoryEntity(BaseModel):
    cod:str
    name:str
    parentCod:str

    def serialize(self) -> dict:
        """Convierte el modelo a dict serializando fechas como string ISO"""
        data = self.model_dump()
        return data