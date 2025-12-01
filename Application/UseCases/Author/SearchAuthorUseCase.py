from logging import getLogger
from typing import List

from Domain.Entities.Author.AuthorEntity import  AuthorEntity
from Infrastructure.DAO.Author.AuthorDAO import AuthorDAO


class SearchAuthorUseCase:
    def __init__(self,dao:AuthorDAO):
        self.log = getLogger("AppLogger")
        self.dao = dao

    async def Execute(self,param:str)->List[AuthorEntity]:
       try:

        res=  await self.dao.search_author(param)
        print("PASEE USE CASE")
        self.log.info("Authors search")
        return res
       except Exception as e:
           self.log.error("Tenemos un error en el caso de uso SearchAuthorUseCase ",e)
           raise e


