from tortoise import Tortoise

from settings import settings


async def init_db():
    await Tortoise.init(
        config=settings.TORTOISE_ORM,
    )
    await Tortoise.generate_schemas()


async def close_db():
    await Tortoise.close_connections()
