from logging import Logger, getLogger
import uuid
from Domain.Entities.Users.UserEntity import  UserEntity
from Application.Helpers.Cipher.HashGeneratorHelper import HashGeneratorHelper
from Infrastructure.DAO.Users.UserDAO import UserDAO


class CreateUserUseCase:
    def __init__(self,dao:UserDAO):
        self.log = getLogger("AppLogger")
        self.dao = dao
        self.cipherHelper = HashGeneratorHelper()
    async def Execute(self,entity:UserEntity)->bool:
       try:
        entity.cod = uuid.uuid4().hex
        entity.first_name=entity.first_name.upper()
        entity.last_name = entity.last_name.upper()
        entity.middle_name = entity.middle_name.upper()
        entity.username = entity.username.upper()
        entity.password_hash = self.cipherHelper.generate(entity.password_hash)
        res=  await self.dao.create_user(entity)
        self.log.info("usuario creado coon exito ")
        return res
       except Exception as e:
           self.log.error("tenemos un error en el caso de uso CreateUserUseCase ")
           raise e


