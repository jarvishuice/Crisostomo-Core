from logging import Logger, getLogger
import uuid
from typing import List, Optional

from Domain.Entities.Author.AuthorEntity import  AuthorEntity
from Application.Helpers.Cipher.HashGeneratorHelper import HashGeneratorHelper
from Infrastructure.DAO.Author.AuthorDAO import AuthorDAO


class GetByCodeUseCase:
    def __init__(self,dao:AuthorDAO):
        self.log = getLogger("AppLogger")
        self.dao = dao

    async def Execute(self,code:str)->Optional[AuthorEntity]:
       try:

        res=  await self.dao.get_author_by_cod(code)
        self.log.info("Authors leidos coon exito ")
        return res
       except Exception as e:
           self.log.error("Tenemos un error en el caso de uso GetByCodeUseCase ")
           raise e


