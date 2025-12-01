from logging import Logger, getLogger
import uuid
from Domain.Entities.Author.AuthorEntity import  AuthorEntity
from Application.Helpers.Cipher.HashGeneratorHelper import HashGeneratorHelper
from Infrastructure.DAO.Author.AuthorDAO import AuthorDAO


class CreateAuthorUseCase:
    def __init__(self,dao:AuthorDAO):
        self.log = getLogger("AppLogger")
        self.dao = dao
        self.cipherHelper = HashGeneratorHelper()
    async def Execute(self,entity:AuthorEntity)->bool:
       try:
        entity.cod = uuid.uuid4().hex
        entity.name =  entity.name.upper()
        if entity.description == None :
            entity.description = "Sin Descripcion"
        entity.description = entity.description.upper()
        res=  await self.dao.create_author(entity)
        self.log.info("Author creado coon exito ")
        return res
       except Exception as e:
           self.log.error("Tenemos un error en el caso de uso CreateAuthorUseCase ")
           raise e


