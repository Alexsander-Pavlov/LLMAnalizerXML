from pydantic import BaseModel
from datetime import date


class AnswerSchema(BaseModel):
    """
    Схема ответа от LLM модели
    """
    uid: int
    date: date
    answer: str
