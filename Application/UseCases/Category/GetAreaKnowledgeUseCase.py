from logging import getLogger
from typing import List

from Domain.Entities.Category.CategoryEntity import CategoryEntity
from Infrastructure.DAO.Category.CategoryDAO import CategoryDAO


class GetAreaKnowledgeUseCase:
    def __init__(self, dao: CategoryDAO):
        self.log = getLogger("AppLogger")
        self.dao = dao

    async def Execute(self) -> List[CategoryEntity]:
        try:

            res = await self.dao.get_by_parent('-1')
            self.log.info("leyendo las areas de conocimiento ")
            return res
        except Exception as e:
            self.log.error("Tenemos un error en el caso de uso GetAreaKnowledgeUseCase ")
            raise e
