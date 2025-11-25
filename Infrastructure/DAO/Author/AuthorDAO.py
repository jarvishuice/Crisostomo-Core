from logging import getLogger
from typing import List, Optional

from Domain.Entities.Author.AuthorEntity import AuthorEntity
from Domain.IDAO.Author.IAuthorDAO import IAuthorDAO
from Infrastructure.Providers.PostgreSQLPoolMaster import PostgreSQLPoolMaster


class AuthorDAO(IAuthorDAO):
    def __init__(self,db: PostgreSQLPoolMaster=None):
        self.db = PostgreSQLPoolMaster.get_instance()
        self.logger = getLogger(__name__)

    async def get_all_authors(self) -> List[AuthorEntity]:
        """Devuelve todos los autores"""
        query = """
                SELECT cod, "name" as name_author, description, created_at, updated_at
                FROM public.author; 
                """

        try:
            async with await self.db.get_connection() as conn:
                # Configuramos cursor para obtener diccionarios
                async with conn.cursor(cursor_factory=self.db.DictCursor) as cur:
                    await cur.execute(query)
                    rows = await cur.fetchall()

            authors: List[AuthorEntity] = [
                self._map_row_to_entity(row) for row in rows
            ]

            self.logger.info(f"Autores cargados correctamente: {len(authors)} encontrados")
            return authors

        except Exception as e:
            self.logger.error(f"Error obteniendo todos los autores: {e}")
            return []

    async def get_author_by_cod(self, cod: str) -> Optional[AuthorEntity]:
        """Devuelve un autor por su código"""
        pass


    async def search_author(self, param: str) -> Optional[List[AuthorEntity]]:
        """Devuelve una  lista deautores por su nombre o descripcion"""
        pass

    async def create_author(self, author: AuthorEntity) -> bool:
        """Crea un nuevo autor"""
        query = """
                INSERT INTO public.author (cod, "name", description, created_at, updated_at)
                VALUES (%s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP) \
                """
        params = (
            author.cod,
            author.name,
            author.description
        )

        try:
            async with await self.db.get_connection() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(query, params)

            self.logger.info(f"Autor '{author.name}' creado correctamente")
            return True

        except Exception as e:
            self.logger.error(f"Error creando autor '{author.name}': {e}")
            return False


    async def update_author(self, author: AuthorEntity) -> bool:
        """Actualiza los datos de un autor existente"""
        pass

    def _map_row_to_entity(self, row) -> AuthorEntity:
        return AuthorEntity(
            cod=row["cod"],
            name=row["name_author"],
            description=row.get("description")
        )