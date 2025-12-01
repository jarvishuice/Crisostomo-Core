from logging import getLogger
from typing import List, Optional

from Domain.Entities.Author.AuthorEntity import AuthorEntity
from Domain.IDAO.Author.IAuthorDAO import IAuthorDAO
from Infrastructure.Providers.PostgreSQLPoolMaster import PostgreSQLPoolMaster
from psycopg.rows import dict_row


class AuthorDAO(IAuthorDAO):
    def __init__(self,db: PostgreSQLPoolMaster=None):
        self.db = PostgreSQLPoolMaster.get_instance()
        self.logger = getLogger("AppLogger")

    async def get_all_authors(self) -> List[AuthorEntity]:
        """Devuelve todos los autores"""
        query = """
                SELECT cod, "name" as name_author, description, created_at, updated_at
                FROM public.author; 
                """

        try:
            async with await self.db.get_connection() as conn:
                # Configuramos cursor para obtener diccionarios
                async with conn.cursor(row_factory=dict_row) as cur:
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
        query =""" SELECT cod, "name" as name_author, description, created_at, updated_at
                FROM public.author WHERE cod = %s;"""
        params = (cod,)
        try:
            async with await self.db.get_connection() as conn:
                # Configuramos cursor para obtener diccionarios
                async with conn.cursor(row_factory=dict_row) as cur:
                    await cur.execute(query,params)
                    rows = await cur.fetchone()

            authors =  self._map_row_to_entity(rows)


            self.logger.info(f"Autores  encontrados")
            return authors
        except Exception as e:
            self.logger.error(f"Error obteniendo   autor por codigo: {e}")
            raise e

    async def search_author(self, param: str) -> List[AuthorEntity]:
        print("PASEEEEE")
        """Devuelve una lista de autores por su nombre o descripción (ILIKE)."""
        query = """
            SELECT cod, "name" AS name_author, description, created_at, updated_at
            FROM public.author
            WHERE "name" ILIKE %s OR description ILIKE %s
            ORDER BY "name" ASC
            LIMIT 100;
        """
        like_param = f"%{param}%"

        try:
            async with await self.db.get_connection() as conn:
                async with conn.cursor(row_factory=dict_row) as cur:
                    await cur.execute(query, (like_param, like_param))
                    rows = await cur.fetchall()

            if not rows:
                self.logger.info(f"No se encontraron autores para: '{param}'")
                raise Exception("No se encontraron autores para: '{param}'")
            authors: List[AuthorEntity] = [self._map_row_to_entity(row) for row in rows]
            self.logger.info(f"Autores encontrados para '{param}': {len(authors)}")
            return authors

        except Exception as e:
            self.logger.error(f"Error buscando autores con '{param}': {e}", exc_info=True)
            raise Exception("Error buscando autores con '{param}': {e}")
        finally:
            self.logger.info("termnine la biusqueda ")

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

        query = """
                 UPDATE public.author
                 SET "name" = %s,
                     description = %s,
                     updated_at = CURRENT_TIMESTAMP
                 WHERE cod = %s
                 """

        params = (
            author.name,
            author.description,
            author.cod
        )

        try:
            async with await self.db.get_connection() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(query, params)

            self.logger.info(f"Autor '{author.cod}' actualizado correctamente")
            return True

        except Exception as e:
            self.logger.error(f"Error actualizando autor '{author.cod}': {e}")
            return False

    def _map_row_to_entity(self, row) -> AuthorEntity:
        return AuthorEntity(
            cod=row["cod"],
            name=row["name_author"],
            description=row.get("description"),
            created_at = row.get("created_at"),
            updated_at= row.get("updated_at"),
        )