from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text
from datetime import date

from config.models import Base


class LLMAnswer(Base):
    """
    Модель ответа LLM
    """
    date: Mapped[date]
    answer: Mapped[str] = mapped_column(Text())
