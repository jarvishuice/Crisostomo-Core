from abc import ABC, abstractmethod


class IDatabasePool(ABC):

    @abstractmethod
    def initialize(self, connection_string: str):
        """
        Inicializa el pool con la cadena de conexión.
        """
        pass

    @abstractmethod
    def get_connection(self):
        """
        Devuelve una conexión activa desde el pool.
        """
        pass

    @abstractmethod
    def release_connection(self, connection):
        """
        Libera una conexión y la devuelve al pool.
        """
        pass

    @abstractmethod
    def close_pool(self):
        """
        Cierra todas las conexiones del pool.
        """
        pass

    @abstractmethod
    def execute(self, query: str, params: tuple = None, fetch: bool = False):
        """
        Ejecuta una consulta rápida (opcional).
        fetch=True devuelve resultados.
        """
        pass
