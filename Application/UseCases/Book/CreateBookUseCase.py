import uuid
from logging import getLogger

from Domain.Entities.Book.BookEntity import BookEntity
from Domain.IDAO.Book.IBookDAO import IBookDAO


class CreateBookUseCase:
    def __init__(self, dao: IBookDAO):
        self.log = getLogger("AppLogger")
        self.dao = dao

    async def Execute(self, entity: BookEntity) -> bool:
        try:

            entity.code = uuid.uuid4().hex
            entity.name = entity.name.upper()
            entity.description = entity.description.upper()
            self.log.info(f"Se le a asigno el codigo {entity.code}")
            return await self.dao.save(entity)
        except Exception as ex:
            self.log.error(ex)
            raise ex
