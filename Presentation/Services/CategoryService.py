from logging import getLogger
from typing import List

from Application.UseCases.Category.FilterByParentCodeUseCase import FilterByParentCodeUseCase
from Application.UseCases.Category.GetAreaKnowledgeUseCase import GetAreaKnowledgeUseCase
from Domain.Entities.Category.CategoryEntity import CategoryEntity
from Infrastructure.DAO.Category.CategoryDAO import CategoryDAO


class CategoryService:
    def __init__(self, dao: CategoryDAO):
        self.dao = dao
        self.__log = getLogger("AppLogeer")
        self.__GetAreas = GetAreaKnowledgeUseCase(dao)
        self.__FilterParentCod = FilterByParentCodeUseCase(dao)

    async def getAreas(self) -> List[CategoryEntity]:
        try:
           return await  self.__GetAreas.Execute()
        except Exception as e:
            self.__log.error(e)
            raise e

    async def getByParentCod(self,parentCod:str)->List[CategoryEntity]:
        try:
            return await self.__FilterParentCod.Execute(parentCod)
        except Exception as e:
            self.__log.error(e)
            raise e