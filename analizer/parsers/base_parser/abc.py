from io import TextIOWrapper
from collections.abc import Sequence
from abc import ABC, abstractmethod
from typing import ClassVar, Generator, Callable
from xml.dom.minidom import Document


class AbstractXMLParser(ABC, Sequence):
    """
    Абстрактный класс XML Парсера
    """
    PARSER: ClassVar[Callable[[str | TextIOWrapper], Document] | None] = None

    @classmethod
    @abstractmethod
    def get_parser(cls) -> Callable[[str | TextIOWrapper], Document] | None:
        pass

    @property
    @abstractmethod
    def attrs(self) -> dict[str, str]:
        pass

    @abstractmethod
    def get_list(self) -> list[dict[str, str]] | None:
        pass

    @abstractmethod
    def get_generator(self) -> Generator[dict[str, str], None, None] | None:
        pass
