from typing import List
from typing import Sequence

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def configure_cors_middleware(
    app: FastAPI,
    allow_origins: Sequence[str],
    allow_credentials: bool,
    allow_methods: Sequence[str] = ("*", ),
    allow_headers: Sequence[str] = ("*", ),
) -> None:
    app.add_middleware(
        CORSMiddleware, # для корректной работы с фронтэндом, нужно именно для бразера, т.к. при отправке запроса из браузера, ему необходимо убедиться, что запрос поступает от доверенного источника
        allow_origins=allow_origins,
        allow_credentials=allow_credentials,
        allow_methods=allow_methods,
        allow_headers=allow_headers,
    )
