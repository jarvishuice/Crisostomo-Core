from pydantic import BaseModel


class AuthorUpdate(BaseModel):
    cod:str
    description: str