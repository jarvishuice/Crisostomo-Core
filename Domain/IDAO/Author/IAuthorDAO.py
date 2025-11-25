from abc import ABC, abstractmethod
from typing import List, Optional
from Domain.Entities.Author import AuthorEntity

class IAuthorDAO(ABC):
    @abstractmethod
    async def get_all_authors(self) -> List[AuthorEntity]:
        """Devuelve todos los autores"""
        pass

    @abstractmethod
    async def get_author_by_cod(self, cod: str) -> Optional[AuthorEntity]:
        """Devuelve un autor por su código"""
        pass

    @abstractmethod
    async def search_author(self, param: str) -> Optional[List[AuthorEntity]]:
        """Devuelve una  lista deautores por su nombre o descripcion"""
        pass

    @abstractmethod
    async def create_author(self, author: AuthorEntity) -> bool:
        """Crea un nuevo autor"""
        pass

    @abstractmethod
    async def update_author(self, author: AuthorEntity) -> bool:
        """Actualiza los datos de un autor existente"""
        pass


