from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi import Request
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi_csrf_protect.exceptions import CsrfProtectError

from src.core.logger import log
from src.lifespan_app import Lifespan
from src.middlewares import configure_cors_middleware

lifespan_manager = Lifespan()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await lifespan_manager.startup()
    yield
    # Shutdown
    await lifespan_manager.shutdown()


def configure_app(
    title: str,
    description: str,
) -> FastAPI:
    app = FastAPI(
        title=title,
        description=description,
        lifespan=lifespan
    )

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

    configure_cors_middleware(
        app=app,
        allow_origins=[
            "http://localhost:5500",
            "http://127.0.0.1:5500",
            "http://frontend:5500",
        ],
        allow_credentials=True,
    )

    @app.exception_handler(CsrfProtectError)
    def csrf_protect_exception_handler(request: Request, exc: CsrfProtectError):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

    return app
