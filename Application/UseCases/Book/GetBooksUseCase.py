import uuid
from logging import getLogger
from typing import List

from Domain.Entities.Book.BookEntity import BookEntity
from Domain.IDAO.Book.IBookDAO import IBookDAO


class GetBooksUseCase:
    def __init__(self, dao: IBookDAO):
        self.log = getLogger("AppLogger")
        self.dao = dao

    async def Execute(self, page_size:int=100,page:int=1) -> List[BookEntity]:
        try:

            return await self.dao.all(page_size=page_size, page=page)
        except Exception as ex:
            self.log.error(ex)
            raise ex
