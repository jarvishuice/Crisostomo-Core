from typing import Optional

from pydantic import BaseModel


class  AuthorRequest(BaseModel):
    name:str
    description:Optional[str]