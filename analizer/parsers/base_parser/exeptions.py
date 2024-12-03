class BaseModelNotProvideError(Exception):
    """
    Исключение вызванное использованием базового класса
    """

    pass


class XMLParseError(Exception):
    """
    Исключение вызванное проблемами при парсинге XML
    """

    pass


class NoDataParseError(Exception):
    """
    Исключение вызванное при пустом списке данных
    """

    pass
