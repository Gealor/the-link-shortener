from contextlib import asynccontextmanager

import uvicorn

from src.api import main_router
from src.configure_app import configure_app
from src.core.config import settings

app = configure_app(
    title="Link Shortener",
    description="This is pet-project Link Shortener"
)

app.include_router(main_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.runtime.host,
        port=settings.runtime.port,
        reload=True,
    )
