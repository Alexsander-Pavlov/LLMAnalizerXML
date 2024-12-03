from pydantic import BaseModel
from typing import Literal


class GetDataAnalystSchema(BaseModel):
    """
    Схема получения данных для аналитика
    """
    role: Literal['system', 'user']
    content: str
