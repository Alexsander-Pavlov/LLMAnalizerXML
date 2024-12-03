from datetime import date, datetime
from typing import Any, Iterator
from parsers.base_converter.abc import AbctractTypeConverter
from collections.abc import MutableMapping

from config import settings
from parsers.base_converter.utils import raise_type_convert_error
from parsers.base_converter.exeptions import BaseModelNotProvideError


class BaseTypeConverter(AbctractTypeConverter):
    """
    Базовый класс конвертера типов.

    Этот класс является Базовым и необоходим только для
    переопеределения.

    ### Для определения своего класса парсера нужно указать:

    - Переопределить :class:`BaseTypeConverter.convert`

    Для примера смотрите :class:`parsers.type_converters.DefaultTypeConverter`
    """

    def __init__(self,
                 target: MutableMapping,
                 parse_int: bool = True,
                 parse_float: bool = True,
                 parse_date: bool = True,
                 ) -> None:
        """
        Args:
            target (MutableMapping): Объект в котором необходимо \
                конвертировать типы данных. Объекта типа :class:`typing.MutableMapping`
            parse_int (bool, optional): Конвертация числовых типов. \
                По умолчания `True`.
            parse_float (bool, optional): Конвертация чисел с плавайщей \
                точкой. По умолчания `True`.
            parse_date (bool, optional): Конвертация Времени типа `datetime.date`. \
                По умолчания `True`.
        """
        self.contaiter = dict(target)
        self.parse_int = bool(parse_int)
        self.parse_float = bool(parse_float)
        self.parse_date = bool(parse_date)

    @classmethod
    def convert_float(self, value: str) -> float | None:
        """
        Конвертирование строки в float
        """
        try:
            value = float(value)
        except ValueError:
            raise_type_convert_error(value=value, type_='float')
        return value

    @classmethod
    def convert_int(self, value: str) -> int | None:
        """
        Конвертирование строки в int
        """
        try:
            value = int(value)
        except ValueError:
            raise_type_convert_error(value=value, type_='int')
        return value

    @classmethod
    def convert_date(self, value: str) -> date:
        """
        Конвертирование строки в data формат
        """
        try:
            date_converting = datetime.strptime(value, settings.DATE_FORMAT)
            value = date_converting.date()
        except ValueError:
            raise_type_convert_error(value=value, type_='date')
        return value

    def __getitem__(self, key: Any) -> Any:
        value = self.contaiter[key]
        return value

    def __setitem__(self, key: Any, value: Any) -> None:
        self.contaiter[key] = value

    def __delitem__(self, key: Any) -> None:
        del self.contaiter[key]

    def __len__(self) -> int:
        return len(self.contaiter)

    def __iter__(self) -> Iterator:
        values = self.contaiter.items()
        for key, item in values:
            yield (key, item)

    def convert(self) -> MutableMapping:
        """
        Метод для переопеределения
        """
        raise BaseModelNotProvideError(
            'Вы не можете использовать базовый класс',
        )
