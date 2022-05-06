from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware

from settings import settings


def build_middlewares():
    middlewares = []
    if settings.is_production:
        frontends = [
            settings.SERVER_DOMAIN,
        ]
    else:
        frontends = [
            "http://localhost:3000",
        ]

    middlewares.append(
        Middleware(
            CORSMiddleware,
            allow_origins=frontends,
            # allow_origins=["*"],
            # allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            expose_headers=["Content-Disposition"],
        )
    )
    return middlewares


all = build_middlewares()
