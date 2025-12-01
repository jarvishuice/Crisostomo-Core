from logging import Logger, getLogger
from Infrastructure.DAO.Author.AuthorDAO import AuthorDAO


class UpdateDescriptionUseCase:
    def __init__(self, dao: AuthorDAO):
        self.log = getLogger("AppLogger")
        self.dao = dao

    async def Execute(self, cod: str, description: str) -> bool:
        try:
            author = await self.dao.get_author_by_cod(cod)
            if author is None:
                raise Exception("El autor no se encuentra registrado ")
            author.description = description.upper()
            res = await self.dao.update_author(author)
            if res is False:
                raise Exception("El autor no se puede actualizar ")

            self.log.info("Author actalizado con exito ")
            return res
        except Exception as e:
            self.log.error("Tenemos un error en el caso de uso CreateAuthorUseCase ")
            raise e
