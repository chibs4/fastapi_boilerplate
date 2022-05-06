import logging
import uvicorn
from fastapi import FastAPI

import middleware
import router
import signals

from settings import settings


def run_app():
    logging.basicConfig(level=settings.LOGGING_LEVEL)

    fastapi_params = dict(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        on_startup=signals.startup_callbacks,
        on_shutdown=signals.shutdown_callbacks,
        middleware=middleware.all,
    )
    if settings.is_production:
        # docs is behind password
        app = FastAPI(**fastapi_params, docs_url=None, redoc_url=None, openapi_url=None)
    else:
        # docs is open
        app = FastAPI(**fastapi_params, debug=True)

    app.include_router(router.main)

    if settings.is_production:
        from docs_security import secure_docs

        secure_docs(
            app,
            admin_username=settings.DOCS_ADMIN_USERNAME,
            admin_password=settings.DOCS_ADMIN_PASSWORD,
            **fastapi_params
        )

    return app


if __name__ == "__main__":
    is_dev = settings.ENV == settings.EnvMode.dev
    uvicorn.run(
        "main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        debug=is_dev,
        reload=is_dev,
        log_level=settings.LOGGING_LEVEL.lower(),
    )
else:
    app = run_app()
