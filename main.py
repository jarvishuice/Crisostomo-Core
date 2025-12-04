import asyncio
import threading

import uvicorn

from Config.Settings import Settings
from Infrastructure.Providers.AppLogger import AppLogger
from Infrastructure.Providers.PostgreSQLPoolMaster import PostgreSQLPoolMaster
from fastapi import FastAPI

from Presentation.Delegates.GeneratePreviewImageDelegate import GeneratePreviewImageDelegate
from Presentation.MIddleWare.RequestLoggingMiddleware import RequestLoggingMiddleware
from Presentation.Routes.AuthRouter import AUTH_ROUTER
from Presentation.Routes.AuthorRouter import AUTHOR_ROUTER
from Presentation.Routes.BookRouter import BOOK_ROUTER
from Presentation.Routes.CategoryRouter import CATEGORY_ROUTER
from Presentation.Routes.EditorialRouter import EDITORIAL_ROUTER
from Presentation.Routes.UsersRouter import USER_ROUTER
from fastapi.middleware.cors import CORSMiddleware
# ------------------------------
# Inicializar Settings y Logger
# ------------------------------
settings = Settings()
log = AppLogger(settings.LOG_PATH)
app = FastAPI()
origins = [
    # "http://localhost:3000", # Origen permitido del frontend
    # "https://tu-dominio.com",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Permite todos los métodos HTTP
    allow_headers=["*"], # Permite todos los encabezados
)

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

def start_delegate_loop(minutes: int):
    """Función que corre el loop async en un hilo separado"""
    asyncio.run(GeneratePreviewImageDelegate.run(minutes))

# ------------------------------
# Eventos de ciclo de vida
# ------------------------------
@app.on_event("startup")
async def startup_event():
    log.info("FastAPI inicializado")
    await db_pool.initialize()   # inicializamos el pool aquí
    log.info("PostgreSQLPool inicializado correctamente")


    # asyncio.create_task(GeneratePreviewImageDelegate.run(1))
    log.info("GeneratePreviewImageDelegate corriendo en hilo aparte")

@app.on_event("shutdown")
async def shutdown_event():
    print("🛑 La aplicación se está cerrando...")
    await db_pool.close_pool()   # cerramos el pool de forma segura
    GeneratePreviewImageDelegate.stop()
    log.info("Worker detenido correctamente")
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
app.include_router(EDITORIAL_ROUTER)
app.include_router(BOOK_ROUTER)