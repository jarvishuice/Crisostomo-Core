from Domain.IDAO.Editorial.IEditorialDAO import IEditorialDAO


class GetEditorialByCodeUseCase:
    def __init__(self, dao: IEditorialDAO):
        self.dao = dao

    async def execute(self, code: str):
        editorial = await self.dao.get_editorial_by_code(code)

        if not editorial:
            raise Exception(f"No existe la editorial con código '{code}'")

        return editorial
