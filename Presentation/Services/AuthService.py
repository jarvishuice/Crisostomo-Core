from typing import List

from Application.UseCases.Auth.GetCurrentUserUseCase import GetCurrentUserUseCase
from Application.UseCases.Auth.LoginUseCase import LoginUseCase
from Application.UseCases.Users.CreateUserUseCase import CreateUserUseCase
from Application.UseCases.Users.GetAllUsersUseCase import GetAllUsersUseCase
from Domain.Entities.Users.UserEntity import UserEntity
from Domain.IDAO.Users.IUsersDAO import IUsersDAO
from Infrastructure.DAO.Users.UserDAO import UserDAO
from Presentation.DTOS.Users.UserResponse import UserResponse


class AuthService:
    def __init__(self,dao:UserDAO):
        self.dao = dao
        self.__Login = LoginUseCase(dao)
        self.__GetCurrentUser = GetCurrentUserUseCase(dao)


    async def login(self,username:str,password:str)->str:
        try:
            return await self.__Login.Execute(username,password)
        except Exception as ex:
            raise ex

    async def getCurrentUser(self,token:str)->UserResponse:
        try:
            return await self.__GetCurrentUser.Execute(token)
        except Exception as ex:
            raise ex