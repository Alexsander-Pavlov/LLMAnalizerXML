import re

from config import settings


def check_xml_file(file_: str) -> re.Match | None:
    """
    Проверка файла на тип XML
    """
    return re.match(settings.regex.XML_REGEX, file_)
