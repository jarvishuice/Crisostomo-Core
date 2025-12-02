from abc import ABC, abstractmethod
from typing import List, Optional
from Domain.Entities.Editorial.EditorialEntity import EditorialEntity

class IEditorialDAO(ABC):

    @abstractmethod
    async def get_all_editorials(self) -> List[EditorialEntity]:
        pass

    @abstractmethod
    async def get_editorial_by_code(self, code: str) -> Optional[EditorialEntity]:
        pass

    @abstractmethod
    async def create_editorial(self, editorial: EditorialEntity) -> bool:
        pass

   
