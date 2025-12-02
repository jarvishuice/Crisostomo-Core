import uuid
from logging import getLogger
from typing import List
from Domain.Entities.Book.BookReadEntity import BookReadEntity
from Domain.IDAO.Book.IBookDAO import IBookDAO


class SearchBookUseCase:
    def __init__(self, dao: IBookDAO):
        self.log = getLogger("AppLogger")
        self.dao = dao

    async def Execute(self, param: str) -> List[BookReadEntity]:
        try:

            return await self.dao.search(param.upper())
        except Exception as ex:
            self.log.error(ex)
            raise ex
