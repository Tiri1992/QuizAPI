from fastapi import FastAPI
from app.api import v1

app = FastAPI(
    title="Quiz API",
)

app.include_router(v1.router_v1, prefix="/api/v1")
