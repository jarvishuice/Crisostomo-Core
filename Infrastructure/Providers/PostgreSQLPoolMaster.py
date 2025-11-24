from threading import Lock
from typing import Optional, Any
from psycopg_pool import ConnectionPool
from Domain.kernel.IDatabasePool import IDatabasePool
from logging import getLogger


class PostgreSQLPool(IDatabasePool):
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        """Singleton thread-safe"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(PostgreSQLPool, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self, connection_string: str = None, minconn: int = 1, maxconn: int = 10,appliction_name:str="Sin nombre de app"):
        if getattr(self, "_initialized", False):
            return

        self.logger = getLogger("AppLogger")
        self.connection_string = connection_string
        self.minconn:int = minconn
        self.maxconn:int = maxconn
        self.pool: Optional[ConnectionPool] = None

        if connection_string:
            self.initialize(connection_string,appliction_name)

        self._initialized = True

    # ------------------------------
    # Inicializar pool
    # ------------------------------
    def initialize(self, connection_string: str,application_name: str = None):
        self.connection_string = connection_string
        if application_name:
            if "application_name=" not in self.connection_string:
                if self.connection_string.endswith(" "):
                    self.connection_string += f"application_name={application_name}"
                else:
                    self.connection_string += f" application_name={application_name}"

        try:
            self.pool = ConnectionPool(
                conninfo=self.connection_string,
                min_size=self.minconn,
                max_size=self.maxconn
            )
            self.logger.info("Pool de PostgreSQL inicializado correctamente")
        except Exception as e:
            self.logger.error(f"Error inicializando pool PostgreSQL: {e}")
            raise e

    # ------------------------------
    # Obtener conexión
    # ------------------------------
    def get_connection(self):
        if not self.pool:
            raise Exception("Pool no inicializado")
        return self.pool.connection()

    # ------------------------------
    # Liberar conexión
    # ------------------------------
    def release_connection(self, connection):
        if connection:
            connection.close()  # psycopg_pool devuelve conexión al pool automáticamente
            self.logger.debug("Conexión devuelta al pool")

    # ------------------------------
    # Cerrar todo el pool
    # ------------------------------
    def close_pool(self):
        if self.pool:
            self.pool.close()
            self.logger.info("Pool de PostgreSQL cerrado")

    # ------------------------------
    # Ejecutar consulta rápida
    # ------------------------------
    def execute(self, query: str, params: tuple = None, fetch: bool = False) -> Any:
        if not self.pool:
            raise Exception("Pool no inicializado")
        result = None
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, params or ())
                    if fetch:
                        result = cur.fetchall()
                        self.logger.debug(f"Consulta ejecutada y resultados obtenidos: {len(result)} filas")
                    else:
                        self.logger.debug("Consulta ejecutada correctamente")
            return result
        except Exception as e:
            self.logger.error(f"Error ejecutando consulta: {e} | Query: {query} | Params: {params}")
            raise e
