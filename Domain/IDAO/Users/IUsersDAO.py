from abc import ABC, abstractmethod
from typing import List, Optional
from Domain.Entities.Users.UserEntity import UserEntity

class IUsersDAO(ABC):
    """Interface para Data Access Object de usuarios"""

    @abstractmethod
    async def create_user(self, user: UserEntity) -> bool:
        """Crea un nuevo usuario en la base de datos"""
        pass

    @abstractmethod
    async def get_user_by_cod(self, cod: str) -> Optional[UserEntity]:
        """Obtiene un usuario por su código"""
        pass

    @abstractmethod
    async def get_user_by_username(self, username: str) -> Optional[UserEntity]:
        """Obtiene un usuario por su nombre de usuario"""
        pass

    @abstractmethod
    async def get_all_users(self) -> List[UserEntity]:
        """Devuelve todos los usuarios"""
        pass

    @abstractmethod
    async def update_user(self, user: UserEntity) -> bool:
        """Actualiza los datos de un usuario"""
        pass

    @abstractmethod
    async def delete_user(self, cod: str) -> bool:
        """Elimina un usuario por su código"""
        pass
