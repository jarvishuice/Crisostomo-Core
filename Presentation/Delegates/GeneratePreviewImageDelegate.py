import asyncio
from logging import getLogger

from Application.Helpers.Pdf.PDFPreviewHelper import PDFPreviewHelper
from Domain.IDAO.Book.IBookDAO import IBookDAO
from Infrastructure.DAO.Book.BookDAO import BookDAO
from Config.Settings import Settings
from datetime import datetime
logger = getLogger("AppLogger")


class GeneratePreviewImageDelegate:
    _running = True

    @staticmethod
    async def __task():
        print("init delegate")
        logger.info(f"[{datetime.now()}] Ejecutando tarea asíncrona...")
        settings = Settings()
        helper = PDFPreviewHelper()
        dao: IBookDAO = BookDAO()
        data = await dao.getBooksNoneImgPreview()
        for item in data:
            logger.info(f"Procesando la prevista del libro  -> {item}")
            helper.generate_preview(f"{settings.PDF_PATH}/{item}.pdf", f"{settings.BOOK_IMG_PATH}/{item}.png")
            r=  await dao.checkImg(item)
            if r:
                logger.info("libro marcado como procesado")
            logger.info(f"fin Procesando la prevista del libro  -> {item}")

    @classmethod
    async def run(cls, minutes: int):
        """Loop asíncrono que ejecuta la tarea cada 10 minutos"""
        while cls._running:
            await cls.__task()
            # Esperar 10 minutos antes de la siguiente ejecución
            await asyncio.sleep(minutes * 60)

    @classmethod
    def stop(cls):
        """Detiene la ejecución del loop"""
        cls._running = False
        print("Se solicitó detener la ejecución.")