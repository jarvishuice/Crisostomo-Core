from pydantic import BaseModel


class UserResponse(BaseModel):
    username: str
    email: str
    full_name:str
    age:int
    cod:str
    birth_date:str
