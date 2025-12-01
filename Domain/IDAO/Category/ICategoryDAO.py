from abc import ABC, abstractmethod
from typing import List, Optional
from Domain.Entities.Author import AuthorEntity
from Domain.Entities.Category.CategoryEntity import CategoryEntity


class  ICategoryDAO(ABC):

    @abstractmethod
    async def get_by_parent(self,parentCode:str)->List[CategoryEntity]:
        pass

