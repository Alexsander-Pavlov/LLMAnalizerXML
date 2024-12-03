from xml.parsers.expat import ExpatError


def parse_expat_error(ex: ExpatError) -> str:
    """
    Парсинг сообщения об ошибке ExpatError
    """
    code = ex.code
    line = ex.lineno
    column = ex.offset
    msg = f'Код проблемы {code}: На линии {line} в колонке {column} ошибка'
    return msg
