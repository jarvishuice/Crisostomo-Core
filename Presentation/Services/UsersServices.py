from typing import List

from Application.UseCases.Users.CreateUserUseCase import CreateUserUseCase
from Application.UseCases.Users.GetAllUsersUseCase import GetAllUsersUseCase
from Domain.Entities.Users.UserEntity import UserEntity
from Domain.IDAO.Users.IUsersDAO import IUsersDAO
from Infrastructure.DAO.Users.UserDAO import UserDAO


class UserServices:
    def __init__(self,dao:UserDAO):
        self.dao = dao
        self.__CreateUserUseCase = CreateUserUseCase(dao)
        self.__GetAllUsersUseCase = GetAllUsersUseCase(dao)

    async def createUser(self,entity:UserEntity)->bool:
        try:
            return await self.__CreateUserUseCase.Execute(entity)
        except Exception as ex:
            raise ex

    async def GetAllUsers(self)->List[UserEntity]:
        try:
            return await self.__GetAllUsersUseCase.Execute()
        except Exception as ex:
            raise ex