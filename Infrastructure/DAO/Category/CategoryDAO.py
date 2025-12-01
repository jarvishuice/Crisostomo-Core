from logging import getLogger
from typing import List
from psycopg.rows import dict_row
from typing_extensions import override

from Domain.Entities.Category.CategoryEntity import CategoryEntity
from Domain.IDAO.Category.ICategoryDAO import ICategoryDAO
from Infrastructure.Providers.PostgreSQLPoolMaster import PostgreSQLPoolMaster


class CategoryDAO(ICategoryDAO):
    def __init__(self, db: PostgreSQLPoolMaster = None):
        self.db = PostgreSQLPoolMaster.get_instance()
        self.logger = getLogger(__name__)



    @override
    async def get_by_parent(self, parentCode: str) -> List[CategoryEntity]:
        query = """
                             SELECT cod, "name" as name_category, parentcod
                             FROM public.dewey_classification
                             WHERE parentcod= %s;
                              """
        params_st= (parentCode,)
        try:
            async with await self.db.get_connection() as conn:
                # Configuramos cursor para obtener diccionarios
                async with conn.cursor(row_factory=dict_row) as cur:
                    await cur.execute(query, params_st)
                    rows = await cur.fetchall()

            authors: List[CategoryEntity] = [
                self._map_row_to_entity(row) for row in rows
            ]

            self.logger.info(f"obteniendo categorias por areas de conocimientos #{parentCode}: {len(authors)}")
            return authors

        except Exception as e:
            self.logger.error(f"Error obteniendo categorias por areas de conocimientos: {e}")
            return []

    def _map_row_to_entity(self, row) -> CategoryEntity:
        return CategoryEntity(
            cod=row["cod"],
            name=row["name_category"],
            parentCod=row["parentcod"],
        )
