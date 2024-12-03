from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select, desc
from sqlalchemy.sql import func
from datetime import date
from typing import Iterable, Generator

from .task_types import TD, TemplateFunc
from config.models import Product
from .promts import analysys_prompt


def union_each_one_data(data: TD,
                        data_to_each: Iterable[TD],
                        ) -> Generator[TD, None, None]:
    """
    Функция для объединения сущности с списком других сущностей

    Args:
        data (TD): Сущность применяемая к основной структуре

        data_to_each Iterable[TD]: Основная структрура с
        сущностями для объединения.

        Пример::
            # Cущность для добавления
            data = {'category': 'item'}
            # Целевая структура
            data_to_each = [{
                {'name': 'Name A'},
                {'name': 'Name B'},
            }]
            items = union_each_one_data(
                data=data,
                data_to_each=data_to_each,
            )
            # Вернет в виде генератора в котором будет:
            # [{'category': 'items', 'name': 'Name A'},
            # {'category': 'items', 'name': 'Name B'},]

    Returns:
        Generator[TD, None, None]: Возвращает генератор,
        это необходимо для оптимизации использования памяти.
    """
    for each in data_to_each:
        yield data | each


class ProductPromptMaker:
    """
    Класс генерации запроса для LLM.

    Этот класс неоходим для корректного составления
    запроса для LLM по опереденному шаблону.

    ## Примеры:
    ```python
    from datetime import date
    from task_schedule.promts import analysys_prompt
    from task_schedule.utils import ProductPromptMaker

    session = AsyncSession
    dete = date(2022, 11, 1)
    prompt_maker = ProductPromptMaker(
        session=session,
        date=date,
        template=analysys_prompt,
    )
    prompt = await prompt_maker.get_prompt()
    ```
    """

    model = Product

    def __init__(self,
                 session: AsyncSession,
                 date: date,
                 template: TemplateFunc = analysys_prompt,
                 ) -> None:
        """
        Args:
            session (AsyncSession): Текущая сессия из Базы Данных
            date (date): Дата для выборки из Базы Данных.
            template (TemplateFunc, optional): Шаблон для составления запроса.\
                По умолчанию - :function:`analysys_prompt`.
        """
        self._session = session
        self.date = date
        self.template = template

    async def get_three_best_price(self,
                                   session: AsyncSession,
                                   date: date,
                                   ) -> list:
        """
        Выборка трех лучших продуктов по цене
        """
        stmt = (Select(self.model.name, self.model.quantity)
                .where(self.model.date == date)
                .order_by(desc(self.model.quantity))
                .limit(3))
        result = await session.scalars(statement=stmt)
        return list(result)

    async def get_total_revenue(self,
                                session: AsyncSession,
                                date: date,
                                ) -> object:
        """
        Выборка общей выручки из всех товаров на определенную дату
        """
        stmt = (Select(func.sum(self.model.price * self.model.quantity))
                .where(self.model.date == date))
        result = await session.scalar(statement=stmt)
        return result

    async def get_categories(self,
                             session: AsyncSession,
                             date: date,
                             ) -> list:
        """
        Получение всех уникальных категорий из данной выборки
        """
        stmt = (Select(self.model.category)
                .distinct()
                .where(self.model.date == date))
        result = await session.scalars(statement=stmt)
        return list(result)

    async def get_prompt(self) -> list[dict[str, str]]:
        """
        Получение готового запроса для LLM
        со всеми готовыми данными
        """
        date = self.date.strftime('%Y-%m-%d')
        best_tree = await self.get_three_best_price(
            session=self._session,
            date=self.date,
        )
        best_tree = ', '.join(best_tree)
        revenue = await self.get_total_revenue(
            session=self._session,
            date=self.date,
        )
        revenue = str(revenue)
        categories = await self.get_categories(
            session=self._session,
            date=self.date,
        )
        categories = ', '.join(categories)
        prompt = self.template(
            date=date,
            revenue=revenue,
            products=best_tree,
            categories=categories,
        )
        return prompt
