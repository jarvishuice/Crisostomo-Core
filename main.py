from Config.Settings import Settings
from Infrastructure.Providers.AppLogger import  AppLogger
from pruebaLogs import execute
from Infrastructure.Providers.PostgreSQLPoolMaster import  PostgreSQLPool
settings = Settings()
log = AppLogger(settings.LOG_PATH)
PostgreSQLPool(minconn=4,maxconn=10,connection_string=f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}",appliction_name=settings.APP_NAME)
log.info("Iniciando AppLogger")
print(settings.DB_HOST)
print(settings.APP_NAME)
print(settings.LOG_PATH)

execute()