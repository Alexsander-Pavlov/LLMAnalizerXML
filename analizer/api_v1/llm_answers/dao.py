from config.dao import BaseDAO
from config.models import LLMAnswer


class AnswerDAO(BaseDAO):
    """
    DAO класс для CRUD продуктов
    """

    model = LLMAnswer
