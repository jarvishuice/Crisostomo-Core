import uuid
from abc import ABC
from logging import getLogger
from typing import List

from Domain.Entities.Book.BookEntity import BookEntity
from Domain.Entities.Book.BookReadEntity import BookReadEntity
from Domain.IDAO.Book.IBookDAO import IBookDAO


class GetBooksNoneImgPreviewUseCase:
    def __init__(self, dao: IBookDAO):
        self.log = getLogger("AppLogger")
        self.dao = dao

    async def Execute(self ) -> List[str]:
        try:

            return await self.dao.getBooksNoneImgPreview()
        except Exception as ex:
            self.log.error(ex)
            raise ex
