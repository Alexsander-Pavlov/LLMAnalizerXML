import asyncio
import celery
from typing import Any, Awaitable, Callable
from functools import wraps

from config import settings


class Celery(celery.Celery):
    """
    Инициализация асинхронного Celery
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.loop = asyncio.get_event_loop()

    def task(
        self,
        task: Callable[..., Awaitable] | None = None,
        **opts: Any,
    ) -> Callable:
        create_task = super().task

        def decorator(func: Callable[..., Awaitable]) -> Callable:
            @create_task(**opts)
            @wraps(func)
            def wrapper(*args,
                        loop: asyncio.AbstractEventLoop | None = None,
                        **kwargs,
                        ):
                loop = loop or self.loop
                return loop.run_until_complete(func(*args, **kwargs))
            return wrapper

        if task:
            return decorator(task)
        return decorator


app = Celery(__name__)
app.conf.broker_url = settings.rabbit.broker_url
app.conf.timezone = settings.celery.TIMEZONE
app.conf.broker_connection_retry_on_startup = True
app.autodiscover_tasks(packages=['task_schedule'])
