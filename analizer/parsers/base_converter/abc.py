from abc import ABC, abstractmethod
from datetime import date
from collections.abc import MutableMapping


class AbctractTypeConverter(ABC, MutableMapping):
    """
    Абстрактный класс конвертера типов
    """

    @classmethod
    @abstractmethod
    def convert_float(self,
                      value: str,
                      ) -> float | None:
        pass

    @classmethod
    @abstractmethod
    def convert_int(self,
                    value: str,
                    ) -> int | None:
        pass

    @classmethod
    @abstractmethod
    def convert_date(self,
                     value: str,
                     ) -> date:
        pass

    @abstractmethod
    def convert(self) -> MutableMapping:
        pass
