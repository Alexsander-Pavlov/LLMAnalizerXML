import asyncio
import httpx
import pytest_asyncio
import pytest
import random

from typing import Any, AsyncGenerator
from contextlib import asynccontextmanager
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from sqlalchemy.pool import NullPool
from datetime import date

from config import test_connection, settings, BaseModel
from config import db_connection
from api_v1.routers import register_routers


db_setup = test_connection(
    settings.test_db.url,
    poolclass=NullPool,
)


@pytest.fixture(scope='session', autouse=True)
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


async def override_get_async_session():
    async with db_setup.session() as session:
        yield session


@pytest_asyncio.fixture(scope='session', autouse=True)
async def app() -> AsyncGenerator[LifespanManager, Any]:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        db_setup.engine.url = settings.test_db.url
        async with db_setup.engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.create_all)
        yield
        await db_setup.dispose()
        async with db_setup.engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.drop_all)
        await db_setup.dispose()

    app = FastAPI(docs_url=None,
                  redoc_url=None,
                  lifespan=lifespan,
                  )
    register_routers(app=app)
    app.dependency_overrides[db_connection.session_geter] = override_get_async_session

    async with LifespanManager(app) as manager:
        yield manager.app


@pytest_asyncio.fixture(scope='session')
async def client(app: FastAPI) -> AsyncGenerator[httpx.AsyncClient, Any]:
    current_home = settings.CURRENT_ORIGIN
    current_api = settings.API_PREFIX
    async with httpx.AsyncClient(
        app=app,
        base_url=current_home + current_api,
    ) as client:
        yield client


@pytest_asyncio.fixture()
async def get_async_session():
    async with db_setup.session() as session:
        yield session


@pytest.fixture
def get_list_items():
    values = [
        {'id': random.randint(1, 21000),
         'name': 'Product A',
         'quantity': 100,
         'price': 1500.00,
         'category': 'Builds',
         'date': date(2024, 1, 1)
         },
        {'id': random.randint(1, 21000),
         'name': 'Product B',
         'quantity': 44,
         'price': 2344.00,
         'category': 'Electronics',
         'date': date(2024, 1, 1)
         },
        {'id': random.randint(1, 21000),
         'name': 'Product C',
         'quantity': 133,
         'price': 666.00,
         'category': 'Machines',
         'date': date(2024, 1, 1)
         },
        {'id': random.randint(1, 21000),
         'name': 'Product D',
         'quantity': 1,
         'price': 150000.00,
         'category': 'Tools',
         'date': date(2024, 1, 1)
         },
        {'id': random.randint(1, 21000),
         'name': 'Product E',
         'quantity': 43,
         'price': 33000.00,
         'category': 'Electronics',
         'date': date(2024, 1, 1)
         },
        {'id': random.randint(1, 21000),
         'name': 'Product G',
         'quantity': 70,
         'price': 5400.00,
         'category': 'Electronics',
         'date': date(2024, 1, 1)
         },
        {'id': random.randint(1, 21000),
         'name': 'Product N',
         'quantity': 900,
         'price': 90.00,
         'category': 'Electronics',
         'date': date(2024, 1, 1)
         },
        {'id': random.randint(1, 21000),
         'name': 'Product L',
         'quantity': 55,
         'price': 2300.00,
         'category': 'Electronics',
         'date': date(2024, 1, 1)
         },
        {'id': random.randint(1, 21000),
         'name': 'Product M',
         'quantity': 10,
         'price': 15000.00,
         'category': 'Electronics',
         'date': date(2024, 1, 1)
         },
    ]
    return values
