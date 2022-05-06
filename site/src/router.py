from fastapi import APIRouter

from routers import *


main = APIRouter()
main.include_router(default_router, prefix="", tags=["Роутер"])
