from logging import getLogger

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import time
from Infrastructure.Providers.AppLogger import AppLogger
from Config.Settings import Settings

settings = Settings()
logger = getLogger("AppLogger")

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # IP del cliente
        client_ip = request.client.host

        # URL solicitada
        url = str(request.url)


        method = request.method

        # User-Agent
        user_agent = request.headers.get("User-Agent", "unknown")

        try:
            response = await call_next(request)
        except Exception as e:
            logger.error(f"ERROR en request {method} {url} desde {client_ip}: {e}")
            raise

        # Tiempo de respuesta
        process_time = (time.time() - start_time) * 1000

        logger.info(
            f"{method} {url} | IP: {client_ip} | "
            f"UA: {user_agent} | {process_time:.2f} ms"
        )

        return response
