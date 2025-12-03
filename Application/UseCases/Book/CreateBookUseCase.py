import uuid
from logging import getLogger

from Domain.Entities.Book.BookEntity import BookEntity
from Domain.IDAO.Book.IBookDAO import IBookDAO


class CreateBookUseCase:
    def __init__(self, dao: IBookDAO):
        self.log = getLogger("AppLogger")
        self.dao = dao

    async def Execute(self, entity: BookEntity, pdf_file) -> bool:
        try:

            entity.code = uuid.uuid4().hex
            entity.name = entity.name.upper()
            entity.description = entity.description.upper()
            self.log.info(f"Se le a asigno el codigo {entity.code}")
            resSave = await self.dao.save(entity)
            if not resSave:
                self.log.info(f"Error al gurdar el libro en base de datos ")
                raise Exception("a ocurrdio un error al guardar el libro")
            self.log.info(f"El libro se guardado en base de datos ")

            resPdf = await self.dao.save_pdf(pdf_file, entity.code)
            if not resPdf:
                self.log.info(f"Error al guardar el  archivo pdf")
            return resPdf

        except Exception as ex:
            self.log.error(ex)
            raise ex
