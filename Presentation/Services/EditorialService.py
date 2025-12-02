

import logging

from Application.UseCases.Editorial.CreateEditorialUseCase import CreateEditorialUseCase
from Application.UseCases.Editorial.GetAllEditorialUseCase import GetAllEditorialsUseCase
from Application.UseCases.Editorial.GetEditorialByCodeUseCase import GetEditorialByCodeUseCase
from Domain.Entities.Editorial.EditorialEntity import EditorialEntity
from Domain.IDAO.Editorial.IEditorialDAO import IEditorialDAO

logger = logging.getLogger("EditorialService")

class EditorialService:

    def __init__(self, dao: IEditorialDAO):
        self.dao = dao
        self.create_uc = CreateEditorialUseCase(dao)
        self.get_by_code_uc = GetEditorialByCodeUseCase(dao)
        self.get_all_uc = GetAllEditorialsUseCase(dao)

    async def create_editorial(self, editorial: EditorialEntity) -> bool:
        try:
            return await self.create_uc.Execute(editorial)
        except Exception as ex:
            logger.error(f"Error creando editorial '{editorial.name}': {ex}")
            raise



    async def get_editorial(self, code: str) -> EditorialEntity:
        try:
            return await self.get_by_code_uc.execute(code)
        except Exception as ex:
            logger.error(f"Error obteniendo editorial '{code}': {ex}")
            raise

    async def get_all_editorials(self):
        try:
            return await self.get_all_uc.execute()
        except Exception as ex:
            logger.error(f"Error obteniendo todas las editoriales: {ex}")
            raise
