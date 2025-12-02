import uvicorn

from Config.Settings import Settings
from Infrastructure.Providers.AppLogger import AppLogger
from Infrastructure.Providers.PostgreSQLPoolMaster import PostgreSQLPoolMaster
from fastapi import FastAPI

from Presentation.MIddleWare.RequestLoggingMiddleware import RequestLoggingMiddleware
from Presentation.Routes.AuthRouter import AUTH_ROUTER
from Presentation.Routes.AuthorRouter import AUTHOR_ROUTER
from Presentation.Routes.CategoryRouter import CATEGORY_ROUTER
from Presentation.Routes.UsersRouter import USER_ROUTER

# ------------------------------
# Inicializar Settings y Logger
# ------------------------------
settings = Settings()
log = AppLogger(settings.LOG_PATH)
app = FastAPI()

log.info("Iniciando AppLogger")

print("Host:", settings.DB_HOST)
print("App Name:", settings.APP_NAME)
print("Log Path:", settings.LOG_PATH)

# Instancia del pool (Singleton)
db_pool = PostgreSQLPoolMaster(
    user=settings.DB_USER,
    password=settings.DB_PASSWORD,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    dbname=settings.DB_NAME,
    minconn=20,
    maxconn=50,
    application_name=settings.APP_NAME,
)

# ------------------------------
# Eventos de ciclo de vida
# ------------------------------
@app.on_event("startup")
async def startup_event():
    log.info("FastAPI inicializado")
    await db_pool.initialize()   # inicializamos el pool aquí
    log.info("PostgreSQLPool inicializado correctamente")

@app.on_event("shutdown")
async def shutdown_event():
    print("🛑 La aplicación se está cerrando...")
    await db_pool.close_pool()   # cerramos el pool de forma segura
@app.get("/")
def index():
    return {"Hello": "World"}
app.add_middleware(RequestLoggingMiddleware)
# ------------------------------
# Routers
# ------------------------------
app.include_router(USER_ROUTER)
app.include_router(AUTH_ROUTER)
app.include_router(AUTHOR_ROUTER)
app.include_router(CATEGORY_ROUTER)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)