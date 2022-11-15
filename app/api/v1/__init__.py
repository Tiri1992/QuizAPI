from fastapi import APIRouter
from app.api.v1.routers import hello
from app.api.v1.routers import user
from app.api.v1.routers import auth

router_v1 = APIRouter()
router_v1.include_router(hello.router)
router_v1.include_router(user.user_router)
router_v1.include_router(auth.auth_router)
