import uuid
from logging import getLogger
from typing import List

from Domain.Entities.Book.BookEntity import BookEntity
from Domain.Entities.Book.BookReadEntity import BookReadEntity
from Domain.IDAO.Book.IBookDAO import IBookDAO


class GetByCategoryUseCase:
    def __init__(self, dao: IBookDAO):
        self.log = getLogger("AppLogger")
        self.dao = dao

    async def Execute(self, category:str) -> List[BookReadEntity]:
        try:

            return await self.dao.get_by_category(category)
        except Exception as ex:
            self.log.error(ex)
            raise ex
