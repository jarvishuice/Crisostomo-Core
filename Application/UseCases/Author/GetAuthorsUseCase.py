from logging import Logger, getLogger
import uuid
from typing import List

from Domain.Entities.Author.AuthorEntity import  AuthorEntity
from Application.Helpers.Cipher.HashGeneratorHelper import HashGeneratorHelper
from Infrastructure.DAO.Author.AuthorDAO import AuthorDAO


class GetAuthorsUseCase:
    def __init__(self,dao:AuthorDAO):
        self.log = getLogger("AppLogger")
        self.dao = dao
        self.cipherHelper = HashGeneratorHelper()
    async def Execute(self)->List[AuthorEntity]:
       try:

        res=  await self.dao.get_all_authors()
        self.log.info("Authors leidos coon exito ")
        return res
       except Exception as e:
           self.log.error("Tenemos un error en el caso de uso GetAuthorsUseCase ")
           raise e


