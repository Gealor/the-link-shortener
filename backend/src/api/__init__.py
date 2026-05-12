from fastapi import APIRouter

from .links import router as link_router

list_routers = (
    link_router,
)

main_router = APIRouter(prefix="/api")

for router in list_routers:
    main_router.include_router(router)

