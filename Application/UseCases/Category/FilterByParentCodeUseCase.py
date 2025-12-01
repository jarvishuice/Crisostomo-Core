from logging import getLogger
from typing import List

from Domain.Entities.Category.CategoryEntity import CategoryEntity
from Infrastructure.DAO.Category.CategoryDAO import CategoryDAO


class FilterByParentCodeUseCase:
    def __init__(self, dao: CategoryDAO):
        self.log = getLogger("AppLogger")
        self.dao = dao

    async def Execute(self,cod:str) -> List[CategoryEntity]:
        try:

            res = await self.dao.get_by_parent(cod)
            self.log.info(f"fi;ltrando categoria por parentCode -> {cod} ")
            return res
        except Exception as e:
            self.log.error("Tenemos un error en el caso de uso FilterByParentCodeUseCase ")
            raise e
