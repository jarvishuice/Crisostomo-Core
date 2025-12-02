from logging import getLogger
from typing import List, Optional
from typing_extensions import override
from Domain.Entities.Editorial.EditorialEntity import EditorialEntity
from Domain.IDAO.Editorial.IEditorialDAO import IEditorialDAO
from Infrastructure.Providers.PostgreSQLPoolMaster import PostgreSQLPoolMaster


class EditorialDAO(IEditorialDAO):
    def __init__(self, db: PostgreSQLPoolMaster = None):
        self.db = PostgreSQLPoolMaster.get_instance()
        self.logger = getLogger('AppLogger')

    @override
    async def get_all_editorials(self) -> List[EditorialEntity]:
        query = """
              SELECT code, name, description, created_at
              FROM public.editorial
              ORDER BY name ASC;
          """

        try:
            async with await self.db.get_connection() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(query)
                    rows = await cur.fetchall()

            result = [self._map_row_to_entity(r) for r in rows]
            self.logger.info(f"Editoriales cargadas correctamente: {len(result)} encontradas")

            return result

        except Exception as e:
            self.logger.error(f"Error obteniendo editoriales: {e}")
            return []

    @override
    async def get_editorial_by_code(self, code: str) -> Optional[EditorialEntity]:
        query = """
            SELECT code, name, description, created_at
            FROM public.editorial
            WHERE code = %s;
        """

        try:
            async with await self.db.get_connection() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(query, (code,))
                    row = await cur.fetchone()

            return self._map_row_to_entity(row) if row else None

        except Exception as e:
            self.logger.error(f"Error obteniendo editorial '{code}': {e}")
            return None

    @override
    async def create_editorial(self, editorial: EditorialEntity) -> bool:
        query = """
              INSERT INTO public.editorial (code, name, description)
              VALUES (%s, %s, %s)
              ON CONFLICT (name) DO NOTHING;
           """

        params = (
            editorial.code,
            editorial.name,
            editorial.description
        )

        try:
            async with await self.db.get_connection() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(query, params)

            self.logger.info(f"Editorial '{editorial.name}' creada correctamente")
            return True

        except Exception as e:
            self.logger.error(f"Error creando editorial '{editorial.code}': {e}")
            return False

    def _map_row_to_entity(self, row) -> EditorialEntity:
        return EditorialEntity(
            code=row[0],
            name=row[1],
            description=row[2],
            created_at=row[3]
        )

