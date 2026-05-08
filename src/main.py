import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import main_router
from core.config import settings

app = FastAPI(
    title="Link Shortener",
    description="This is pet-project Link Shortener"
)

origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost",
    "http://127.0.0.1",
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
