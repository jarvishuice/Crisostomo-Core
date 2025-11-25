from threading import Lock
from typing import Optional, Any
from psycopg_pool import AsyncConnectionPool
from logging import getLogger
import asyncio

class PostgreSQLPoolMaster:
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        """Singleton thread-safe"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(PostgreSQLPoolMaster, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    @classmethod
    def get_instance(cls):
        if cls._instance is None:

            raise Exception("PoolMaster aún no ha sido inicializado")
        return cls._instance
    def __init__(
        self,
        user: str,
        password: str,
        host: str,
        port: int,
        dbname: str,
        minconn: int = 1,
        maxconn: int = 10,
        application_name: str = "Sin nombre de app",
    ):
        if getattr(self, "_initialized", False):
            return

        self.logger = getLogger("AppLogger")
        self.user = user
        self.password = password
        self.host = host
        self.port = int(port)
        self.dbname = dbname
        self.minconn = int(minconn)
        self.maxconn = int(maxconn)
        self.application_name = application_name

        self.pool: Optional[AsyncConnectionPool] = None

        self._initialized = True

    async def initialize(self):
        """Inicializa el pool dentro de un loop asíncrono"""
        if self.pool:
            return  # ya inicializado
        try:
            conninfo = (
                f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}"
                f"?application_name={self.application_name}"
            )
            self.pool = AsyncConnectionPool(
                conninfo=conninfo,
                min_size=self.minconn,
                max_size=self.maxconn
            )
            # Abrimos el pool dentro del loop
            await self.pool.open()
            self.logger.info(f"Async Pool de PostgreSQL '{self.application_name}' inicializado correctamente")
        except Exception as e:
            self.logger.error(f"Error inicializando async pool PostgreSQL: {e}")
            raise e

    async def get_connection(self):
        if not self.pool:
            raise Exception("Pool no inicializado, llama primero a initialize()")
        return self.pool.connection()  # devuelve un context manager async

    async def execute(self, query: str, params: tuple = None, fetch: bool = False) -> Any:
        if not self.pool:
            raise Exception("Pool no inicializado, llama primero a initialize()")
        result = None
        try:
            async with await self.get_connection() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(query, params or ())
                    if fetch:
                        result = await cur.fetchall()
            return result
        except Exception as e:
            self.logger.error(f"Error ejecutando consulta async: {e} | Query: {query} | Params: {params}")
            raise e

    async def close_pool(self):
        if self.pool:
            await self.pool.close()
            self.logger.info(f"Async Pool de PostgreSQL '{self.application_name}' cerrado")


