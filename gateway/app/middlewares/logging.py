# gateway/app/middlewares/logging.py
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import logging

logger = logging.getLogger("gateway")

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info(f"Получен запрос: {request.method} {request.url}")
        response = await call_next(request)
        logger.info(f"Ответ: {response.status_code}")
        return response
