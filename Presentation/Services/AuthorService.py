from logging import getLogger
from typing import List, Optional
from Application.UseCases.Author.CreateAuthorUseCase import CreateAuthorUseCase
from Application.UseCases.Author.GetAuthorsUseCase import GetAuthorsUseCase
from Application.UseCases.Author.GetByCodeUseCase import GetByCodeUseCase
from Application.UseCases.Author.SearchAuthorUseCase import SearchAuthorUseCase
from Application.UseCases.Author.UpdateDescriptionUseCase import UpdateDescriptionUseCase
from Domain.Entities.Author.AuthorEntity import AuthorEntity
from Infrastructure.DAO.Author.AuthorDAO import AuthorDAO


class AuthorService:
    def __init__(self, dao: AuthorDAO):
        self.dao = dao
        self.__log = getLogger("AppLogeer")
        self.__CreateAuthor = CreateAuthorUseCase(dao)
        self.__GetAuthors = GetAuthorsUseCase(dao)
        self.__GetAuthor = GetByCodeUseCase(dao)
        self.__SearchAuthor = SearchAuthorUseCase(dao)
        self.__UpdateDescripton = UpdateDescriptionUseCase(dao)

    async def create(self, name: str, description: str = "sin descripciopn") -> bool:
        try:
            entity: AuthorEntity = AuthorEntity(cod="sss", name=name, description=description)
            return await self.__CreateAuthor.Execute(entity)

        except Exception as ex:
            raise ex

    async def update(self, cod: str, description: str = "sin descripciopn") -> bool:
        try:

            return await self.__UpdateDescripton.Execute(cod, description)

        except Exception as ex:
            raise ex

    async def getAll(self) -> List[AuthorEntity]:
        try:

            return await self.__GetAuthors.Execute()

        except Exception as ex:
            raise ex

    async def getAuthor(self, code: str) -> Optional[AuthorEntity]:
        try:
            return await self.__GetAuthor.Execute(code)
        except Exception as ex:
            raise ex

    async def search(self, param: str) -> List[AuthorEntity]:
        try:
            self.__log.info("parase por el servicio")
            return await self.__SearchAuthor.Execute(param)
        except Exception as ex:
            raise ex
