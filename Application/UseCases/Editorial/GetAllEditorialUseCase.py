from Domain.IDAO.Editorial.IEditorialDAO import IEditorialDAO


class GetAllEditorialsUseCase:
    def __init__(self, dao: IEditorialDAO):
        self.dao = dao

    async def execute(self):
        try:
            return await self.dao.get_all_editorials()
        except Exception as e:
            raise e