from contextlib import asynccontextmanager
from fastapi import FastAPI

from api_v1 import register_routers
from app_includes import (
    register_errors,
    register_middlewares,
    )
from llm_analizer import Qwen


def start_app() -> FastAPI:
    """
    Создание приложения со всеми настройками
    """
    Qwen.load_model()
    app = FastAPI(lifespan=lifespan)
    register_routers(app=app)
    register_errors(app=app)
    register_middlewares(app=app)
    return app


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = start_app()
