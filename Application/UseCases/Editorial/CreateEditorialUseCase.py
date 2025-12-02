import uuid


from Domain.Entities.Editorial.EditorialEntity import EditorialEntity
from Domain.IDAO.Editorial.IEditorialDAO import IEditorialDAO
from . import  logs

class CreateEditorialUseCase:
    def __init__(self, dao: IEditorialDAO):
        self.dao = dao

    async def Execute(self, entity: EditorialEntity) -> bool:
        try:

            entity.code = uuid.uuid4().hex
            entity.name = entity.name.upper()
            if entity.description is not None:
                entity.description = entity.description.upper()
            else:
                entity.description = "SIN DESC"




            return await self.dao.create_editorial(entity)

        except Exception as e:
            raise Exception(e)


