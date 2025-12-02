from logging import getLogger
from typing import List

from Application.UseCases.Book.CreateBookUseCase import CreateBookUseCase
from Application.UseCases.Book.GetBookByAreaUseCase import GetBookByAreaUseCase
from Application.UseCases.Book.GetBooksUseCase import GetBooksUseCase
from Application.UseCases.Book.GetByCategoryUseCase import GetByCategoryUseCase
from Application.UseCases.Book.GetBySubAreaUseCase import GetBySubAreaUseCase
from Application.UseCases.Book.SearchBookUseCase import SearchBookUseCase
from Domain.Entities.Book.BookEntity import BookEntity
from Domain.Entities.Book.BookReadEntity import BookReadEntity
from Domain.IDAO.Book.IBookDAO import IBookDAO


class BookService:
    def __init__(self, dao: IBookDAO):
        self.dao = dao
        self.__log = getLogger("AppLogeer")
        self.__SaveBook = CreateBookUseCase(dao)
        self.__GetBook = GetBooksUseCase(dao)
        self.__GetByCategory = GetByCategoryUseCase(dao)
        self.__GetBySubArea = GetBySubAreaUseCase(dao)
        self.__GetByArea = GetBookByAreaUseCase(dao)
        self.__SearchBook = SearchBookUseCase(dao)

    async def getByArea(self, area: str) -> List[BookReadEntity]:
        try:
            return await self.__GetByArea.Execute(area)

        except Exception as e:
            self.__log.error(e)
            raise e

    async def getBySubArea(self, subArea: str) -> List[BookReadEntity]:
        try:
            return await self.__GetBySubArea.Execute(subArea)

        except Exception as e:
            self.__log.error(e)
            raise e

    async def getByCategory(self, category: str) -> List[BookReadEntity]:
        try:
            return await self.__GetByCategory.Execute(category)

        except Exception as e:
            self.__log.error(e)
            raise e
    async def search(self, param: str) -> List[BookReadEntity]:
        try:
            return await self.__SearchBook.Execute(param)

        except Exception as e:
            self.__log.error(e)
            raise e

    async def save(self, entity: BookEntity) -> bool:
        try:
            return await self.__SaveBook.Execute(entity)
        except Exception as e:
            self.__log.error(e)
            raise e

    async def get_books(self, page_size: int = 100, page: int = 1) -> List[BookEntity]:
        try:
            return await self.__GetBook.Execute(page_size, page)
        except Exception as e:
            self.__log.error(e)
            raise e
