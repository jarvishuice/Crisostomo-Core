import os
from dotenv import load_dotenv
from threading import Lock


class Settings:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        """Singleton thread-safe"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(Settings, cls).__new__(cls)
                    cls._instance._load_env()
        return cls._instance

    def _load_env(self):
        """Carga el archivo .env una sola vez"""
        load_dotenv()

        # Configuración general
        self.APP_NAME = os.getenv("APP_NAME", "Biblioteca Digital")
        self.APP_ENV = os.getenv("APP_ENV", "development")
        self.APP_DEBUG = os.getenv("APP_DEBUG", "True").lower() == "true"
        self.APP_PORT = int(os.getenv("APP_PORT", "8000"))

        # Config DB
        self.DB_HOST = os.getenv("DB_HOST")
        self.DB_PORT = int(os.getenv("DB_PORT", "5432"))
        self.DB_NAME = os.getenv("DB_NAME")
        self.DB_USER = os.getenv("DB_USER")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD")

        self.DATABASE_URL = os.getenv("DATABASE_URL")

        # Logs
        self.LOG_PATH = os.getenv("LOG_PATH", "logs/app.log")
        self.LOG_SQL_PATH = os.getenv("LOG_SQL_PATH", "logs/sql.log")

        # Seguridad
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
        self.ALGORITHM = os.getenv("ALGORITHM", "HS256")
        self.ACCESS_TOKEN_EXPIRE_HOURS = int(os.getenv("ACCESS_TOKEN_EXPIRE_HOURS", "8"))
        self.AUTHOR_IMG_PATH = os.getenv("AUTHOR_IMG_PATH", "./NOLOCONSEGUI")
        self.BOOK_IMG_PATH = os.getenv("BOOK_IMG_PATH", "./NOLOCONSEGUI")
        self.PDF_PATH = os.getenv("PDF_PATH", "./NOLOCONSEGUI")
        self.USER_PROFILE_IMG_PATH = os.getenv("USER_PROFILE_IMG_PATH", "./NOLOCONSEGUI")


    def __repr__(self):
        return f"<Settings env={self.APP_ENV} debug={self.APP_DEBUG}>"
