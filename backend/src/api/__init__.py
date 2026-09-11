from fastapi import APIRouter

from .auth import router as auth_router
from .links import router as link_router
from .test import router as test_router

list_routers = (
    auth_router,
    link_router,
    test_router,
)

main_router = APIRouter(prefix="/api")

for router in list_routers:
    main_router.include_router(router)
