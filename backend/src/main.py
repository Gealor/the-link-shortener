from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi import Request
from fastapi import status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.api import main_router
from src.core.config import settings
from src.core.logger import log
from src.lifespan_app import Lifespan

lifespan_manager = Lifespan()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await lifespan_manager.startup()
    yield
    # Shutdown
    await lifespan_manager.shutdown()


app = FastAPI(
    title="Link Shortener",
    description="This is pet-project Link Shortener",
    lifespan=lifespan
)

# Это middleware (а не exception_handler), чтобы CORSMiddleware, добавленный ниже и потому
# внешний, успел навесить свои заголовки на ответ с ошибкой.
@app.middleware("http")
async def catch_unhandled_exceptions(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception:
        log.exception("Unhandled error: %s %s", request.method, request.url.path)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error. Please try again later."},
        )


origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://frontend:5500",
] # адреса, где расположен фронтэнд, чтобы CORS выполнил запросы к API, отправленные с этих адресов

app.add_middleware(
    CORSMiddleware, # для корректной работы с фронтэндом, нужно именно для бразера, т.к. при отправке запроса из браузера, ему необходимо убедиться, что запрос поступает от доверенного источника
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.runtime.host,
        port=settings.runtime.port,
        reload=True,
    )
