import pytest
import datetime

from task_schedule.promts import analysys_prompt
from task_schedule.utils import ProductPromptMaker
from api_v1.products.dao import ProductDAO


@pytest.mark.prompt
def test_text_prompt():
    date = datetime.date(2024, 1, 1).strftime('%Y-%m-%d')
    revenue = '10033.33'
    products = 'Iphone, MacBook'
    categories = 'Phones, Computers'
    prompt = analysys_prompt(
        date=date,
        revenue=revenue,
        products=products,
        categories=categories,
    )
    assert [
        dict(
            role='system',
            content='You are the best data analyst.',
        ),
        dict(
            role='user',
            content="""Analyze sales data for 2024-01-01:
1. Total revenue: 10033.33 RUB.
2. Top 3 products by sales: Iphone, MacBook.
3. Distribution by categories: Phones, Computers.
Write a short analytical report with conclusions and recommendations.
This is very important for my career""",
        )
    ] == prompt


@pytest.mark.asyncio
async def test_prompt_maker_best(client, get_async_session, get_list_items):
    values = (value for value in get_list_items)
    await ProductDAO.add_multiple(session=get_async_session,
                                  list_values=values,
                                  )
    date = datetime.date(2024, 1, 1)
    three_best = await (ProductPromptMaker(
        session=get_async_session,
        date=date,
        ).get_three_best_price(
            session=get_async_session,
            date=date))
    assert three_best == ['Product N', 'Product C', 'Product A']


@pytest.mark.asyncio
async def test_prompt_maker_total(client, get_async_session, get_list_items):
    date = datetime.date(2024, 1, 1)
    total = await (ProductPromptMaker(
        session=get_async_session,
        date=date,
        ).get_total_revenue(
            session=get_async_session,
            date=date))
    assert total == 2651814.0


@pytest.mark.asyncio
async def test_prompt_maker_categories(client,
                                       get_async_session,
                                       get_list_items,
                                       ):
    date = datetime.date(2024, 1, 1)
    categories = await (ProductPromptMaker(
        session=get_async_session,
        date=date,
        ).get_categories(
            session=get_async_session,
            date=date))
    assert categories == ['Builds',
                          'Category',
                          'Electronics',
                          'Machines',
                          'Tools']


@pytest.mark.asyncio
async def test_prompt_maker(client, get_async_session, get_list_items):
    date = datetime.date(2024, 1, 1)
    prompt = await (ProductPromptMaker(
        session=get_async_session,
        date=date,
        ).get_prompt())
    assert prompt == dict(
        system='You are the best data analyst.',
        user="""Analyze sales data for 2024-01-01:
1. Total revenue: 2651814.0.
2. Top 3 products by sales: Product N, Product C, Product A.
3. Distribution by categories: Builds, Category, Electronics, Machines, Tools.

Write a short analytical report with conclusions and recommendations.
This is very important for my career""",
    )
