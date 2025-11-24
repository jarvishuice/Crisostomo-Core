import logging
import sqlite3
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler
from threading import Lock

from Domain.kernel.ILogger import ILogger
from Config.Settings import Settings


class AppLogger(ILogger):
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        """Singleton thread-safe"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(AppLogger, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self, log_dir: str = None):
        """
        log_dir: ruta donde se almacenarán los logs (sin archivo)
        """
        if self._initialized:
            return

        self.settings = Settings()
        self.log_dir = log_dir or self.settings.LOG_PATH  # ruta base

        os.makedirs(self.log_dir, exist_ok=True)

        # Archivo actual basado en la fecha
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        self.log_file_path = self._generate_daily_log_path()

        self._setup_sqlite()
        self.logger = self._configure_logger()

        self._initialized = True

    # -------------------------------------------------
    # GENERAR ARCHIVO DE LOG POR DÍA
    # -------------------------------------------------
    def _generate_daily_log_path(self):
        filename = f"app_{self.current_date}.log"
        return os.path.join(self.log_dir, filename)

    def _check_date_rollover(self):
        """
        Si cambia el día → actualizar el archivo de logs.
        """
        today = datetime.now().strftime("%Y-%m-%d")
        if today != self.current_date:
            self.current_date = today
            self.log_file_path = self._generate_daily_log_path()
            self._replace_file_handler()

    def _replace_file_handler(self):
        """
        Cambia el archivo del handler sin reiniciar el Logger.
        """
        for handler in self.logger.handlers:
            if isinstance(handler, RotatingFileHandler):
                self.logger.removeHandler(handler)

        new_handler = RotatingFileHandler(
            self.log_file_path,
            maxBytes=5_000_000,
            backupCount=5,
            encoding="utf-8"
        )
        new_handler.setFormatter(self._get_formatter())
        self.logger.addHandler(new_handler)

    # -------------------------------------------------
    # SQLITE CONFIG
    # -------------------------------------------------
    def _setup_sqlite(self):
        sqlite_dir = os.path.join(self.log_dir, "sqlite")
        os.makedirs(sqlite_dir, exist_ok=True)

        self.sqlite_path = os.path.join(sqlite_dir, "logs.db")

        conn = sqlite3.connect(self.sqlite_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                level TEXT,
                message TEXT,
                module TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    # -------------------------------------------------
    # MAIN LOGGER CONFIG
    # -------------------------------------------------
    def _configure_logger(self):
        logger = logging.getLogger("AppLogger")
        logger.setLevel(logging.DEBUG)

        if logger.handlers:
            return logger

        # FILE HANDLER
        file_handler = RotatingFileHandler(
            self.log_file_path,
            maxBytes=5_000_000,
            backupCount=5,
            encoding="utf-8"
        )
        file_handler.setFormatter(self._get_formatter())
        logger.addHandler(file_handler)

        # CONSOLE
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(self._get_formatter())
        logger.addHandler(console_handler)

        # SQLITE HANDLER
        logger.addHandler(self.SQLiteHandler(self.sqlite_path))

        return logger

    def _get_formatter(self):
        return logging.Formatter(
            "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        )

    # -------------------------------------------------
    # MÉTODOS DE LOGGER (con rollover diario)
    # -------------------------------------------------
    def info(self, message: str):
        self._check_date_rollover()
        self.logger.info(message)

    def warning(self, message: str):
        self._check_date_rollover()
        self.logger.warning(message)

    def error(self, message: str):
        self._check_date_rollover()
        self.logger.error(message)

    def debug(self, message: str):
        self._check_date_rollover()
        self.logger.debug(message)

    def critical(self, message: str):
        self._check_date_rollover()
        self.logger.critical(message)

    # -------------------------------------------------
    # SQLITE HANDLER
    # -------------------------------------------------
    class SQLiteHandler(logging.Handler):
        def __init__(self, db_path):
            super().__init__()
            self.db_path = db_path

        def emit(self, record):
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO logs (level, message, module)
                    VALUES (?, ?, ?)
                """, (
                    record.levelname,
                    record.getMessage(),
                    record.module
                ))
                conn.commit()
                conn.close()
            except Exception as e:
                print(f"Error guardando log en SQLite: {e}")
