from typing import Optional, List
from Domain.Entities.Users.UserEntity import UserEntity
from Domain.IDAO.Users.IUsersDAO import IUsersDAO
from Infrastructure.Providers.PostgreSQLPoolMaster import PostgreSQLPoolMaster
from Infrastructure.Providers.AppLogger import AppLogger
from Config.Settings import Settings

settings = Settings()
log = AppLogger(settings.LOG_PATH)


class UserDAO(IUsersDAO):
    def __init__(self,db: PostgreSQLPoolMaster=None):
        self.db = PostgreSQLPoolMaster.get_instance()
        self.logger = log

    async def get_all_users(self) -> List[UserEntity]:
        """Devuelve todos los usuarios"""
        query = "SELECT * FROM app_user ORDER BY created_at DESC"
        users: List[UserEntity] = []

        try:
            async with await self.db.get_connection() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(query)
                    rows = await cur.fetchall()

            for row in rows:
                users.append(self._map_row_to_entity(row))

            self.logger.info(f"Usuarios cargados correctamente: {len(users)} encontrados")
            return users

        except Exception as e:
            self.logger.error(f"Error obteniendo todos los usuarios: {e}")
            return []


    async def create_user(self, user: UserEntity) -> bool:
        query = """
        INSERT INTO app_user (
            cod, first_name, middle_name, last_name, second_last_name,
            email, date_of_birth, phone_number, username, password_hash,
            created_at, updated_at
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)
        """
        params = (
            user.cod,
            user.first_name,
            user.middle_name,
            user.last_name,
            user.second_last_name,
            user.email,
            user.date_of_birth,
            user.phone_number,
            user.username,
            user.password_hash
        )
        try:
            async with await self.db.get_connection() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(query, params)
            self.logger.info(f"Usuario '{user.username}' creado correctamente")
            return True
        except Exception as e:
            self.logger.error(f"Error creando usuario '{user.username}': {e}")
            return False

    async def get_user_by_cod(self, cod: str) -> Optional[UserEntity]:
        query = "SELECT * FROM app_user WHERE cod = %s"
        try:
            async with await self.db.get_connection() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(query, (cod,))
                    row = await cur.fetchone()
            if row:
                return self._map_row_to_entity(row)
            return None
        except Exception as e:
            self.logger.error(f"Error obteniendo usuario por cod '{cod}': {e}")
            return None

    async def get_user_by_username(self, username: str) -> Optional[UserEntity]:
        query = "SELECT * FROM app_user WHERE username = %s"
        try:
            async with await self.db.get_connection() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(query, (username,))
                    row = await cur.fetchone()
            if row:
                return self._map_row_to_entity(row)
            return None
        except Exception as e:
            self.logger.error(f"Error obteniendo usuario por username '{username}': {e}")
            return None

    async def update_user(self, user: UserEntity) -> bool:
        query = """
        UPDATE app_user
        SET first_name=%s, middle_name=%s, last_name=%s, second_last_name=%s,
            email=%s, date_of_birth=%s, phone_number=%s, username=%s, password_hash=%s,
            updated_at=CURRENT_TIMESTAMP
        WHERE cod=%s
        """
        params = (
            user.first_name,
            user.middle_name,
            user.last_name,
            user.second_last_name,
            user.email,
            user.date_of_birth,
            user.phone_number,
            user.username,
            user.password_hash,
            user.cod
        )
        try:
            async with await self.db.get_connection() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(query, params)
            self.logger.info(f"Usuario '{user.username}' actualizado correctamente")
            return True
        except Exception as e:
            self.logger.error(f"Error actualizando usuario '{user.username}': {e}")
            return False

    async def delete_user(self, cod: str) -> bool:
        query = "DELETE FROM app_user WHERE cod=%s"
        try:
            async with await self.db.get_connection() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(query, (cod,))
            self.logger.info(f"Usuario '{cod}' eliminado correctamente")
            return True
        except Exception as e:
            self.logger.error(f"Error eliminando usuario '{cod}': {e}")
            return False

    def _map_row_to_entity(self, row) -> UserEntity:
        return UserEntity(
            cod=row[0],
            first_name=row[1],
            middle_name=row[2],
            last_name=row[3],
            second_last_name=row[4],
            email=row[5],
            date_of_birth=row[6],
            phone_number=row[7],
            username=row[8],
            password_hash=row[9]
        )
