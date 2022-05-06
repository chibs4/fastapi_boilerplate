""" Сахар для работы с ORM """

from typing import Any, Dict, Optional, Tuple, TypeVar

from tortoise import models, fields
from tortoise.backends.base.client import BaseDBAsyncClient
from tortoise.exceptions import DoesNotExist
from tortoise.transactions import in_transaction

# from services.storage.storage import Storage


MODEL = TypeVar("MODEL", bound="models.Model")


class Model(models.Model):
    """Переопределение модели для сахарных патчей"""

    async def update(self, **fields: Dict[str, Any]):
        """Обновляет поля экземпляра класса и сохраняет в БД"""
        self.update_from_dict(fields)
        await self.save(update_fields=fields.keys())
        return self

    @classmethod
    def first(cls, *args, **kwargs) -> MODEL:
        query = super().first().filter(*args, **kwargs)
        query._raise_does_not_exist = True
        return query

    @classmethod
    def first_or_none(cls, *args, **kwargs) -> Optional[MODEL]:
        return super().first().filter(*args, **kwargs)

    @classmethod
    async def get_or_create(
        cls,
        defaults: Optional[dict] = None,
        using_db: Optional[BaseDBAsyncClient] = None,
        **kwargs: Any,
    ) -> Tuple[MODEL, bool]:
        """
        Fetches the object if exists (filtering on the provided parameters),
        else creates an instance with any unspecified parameters as default values.
        :param defaults: Default values to be added to a created instance if it can't be fetched.
        :param using_db: Specific DB connection to use instead of default bound
        :param kwargs: Query parameters.
        UPD:
        1) get() instead of stupid filter().first().
        2) MultipleObjectsReturned, IntegrityError, TransactionManagementError are not
        passed silently.
        """
        if defaults is None:
            defaults = {}
        async with in_transaction(
            connection_name=(using_db or cls._meta.db).connection_name
        ):
            try:
                return await cls.get(**kwargs), False
            except DoesNotExist:
                return await cls.create(**defaults, **kwargs, using_db=using_db), True

    @classmethod
    async def update_or_create(
        cls,
        defaults: Optional[dict] = None,
        using_db: Optional[BaseDBAsyncClient] = None,
        **kwargs: Any,
    ) -> Tuple[MODEL, bool]:
        """
        A convenience method for updating an object with the given kwargs, creating a new one if necessary.
        :param defaults: Default values used to update the object.
        :param using_db: Specific DB connection to use instead of default bound
        :param kwargs: Query parameters.
        UPD:
        1) Redefined to call `update` instead of `save`.
        2) get() instead of stupid filter().first().
        3) MultipleObjectsReturned, IntegrityError, TransactionManagementError are not
        passed silently.
        """
        if defaults is None:
            defaults = {}
        async with in_transaction(
            connection_name=(using_db or cls._meta.db).connection_name
        ):
            try:
                instance = await cls.get(**kwargs)
            except DoesNotExist:
                return await cls.create(**defaults, **kwargs, using_db=using_db), True
            else:
                await instance.update(**defaults)
                return instance, False


# class WithFile:
#     """Миксин для файлов
#     В дочернем классе необходимо объявить поля
#     *_hash = fields.CharField(max_length=64, null=True, unique=True)"""

#     uploaded_at = fields.DatetimeField(auto_now_add=True, null=True)

#     async def update(self, **fields: Dict[str, Any]):
#         """Удаление файла из облака если хеш перезаписан"""
#         # TODO: do this in another task or invent files autocleaner
#         for key in fields:
#             if key.endswith("_hash"):
#                 new_value = fields[key]
#                 if (old_value := getattr(self, key)) and new_value != old_value:
#                     async with Storage() as storage:
#                         await storage.delete(old_value)

#         await super().update(self, **fields)

#     async def delete(self):
#         """Удаление инстанса вместе с файлами"""
#         # TODO: do this in another task or invent files autocleaner
#         for key in self.__dict__:
#             if key.endswith("_hash") and (value := getattr(self, key)):
#                 async with Storage() as storage:
#                     await storage.delete(value)

#         await super().delete(self)

#     def __getattr__(self, key):
#         """Получение file_url для всех файлов"""
#         # TODO: define as cached property?
#         if key.endswith("_url"):
#             file_hash = getattr(self, key[:-4] + "_hash")
#             if file_hash:
#                 return Storage().get_url(file_hash)
#             return None
#         return getattr(super(), key)
