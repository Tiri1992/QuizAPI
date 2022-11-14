from fastapi import APIRouter
from app.api.v1.routers import hello

router_v1 = APIRouter()
router_v1.include_router(hello.router)
