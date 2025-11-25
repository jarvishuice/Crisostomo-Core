from logging import getLogger
from typing import List

from Domain.Entities.Users.UserEntity import UserEntity
from Infrastructure.DAO.Users.UserDAO import UserDAO


class GetAllUsersUseCase:
    def __init__(self,dao:UserDAO):
        self.log = getLogger("AppLogger")
        self.dao = dao


    async def Execute(self)->List[UserEntity]:
       try:

        res=  await self.dao.get_all_users()
        self.log.info("usuario creado coon exito ")
        return res
       except Exception as e:
           self.log.error("tenemos un error en el caso de uso GetAllUsersUseCase ")
           raise e