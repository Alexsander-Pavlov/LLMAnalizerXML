from typing import Iterable, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from config.dao import BaseDAO
from config.models import Product


class ProductDAO(BaseDAO):
    """
    DAO класс для CRUD продуктов
    """
    model = Product

    @classmethod
    async def add_multiple(cls,
                           session: AsyncSession,
                           list_values: Iterable[dict[str, Any]],
                           ) -> list[object]:
        async with session.begin():
            list_items = (cls.model(**value)
                          for value
                          in list_values)
            session.add_all(list_items)
            try:
                await session.commit()
            except SQLAlchemyError as ex:
                await session.rollback()
                raise ex
            return list_items
