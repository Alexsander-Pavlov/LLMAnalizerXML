from starlette.exceptions import HTTPException


class ValidationError(HTTPException):
    """
    Исключение вызванное проблемами с валидацией
    """

    pass


class APIFileNotFoundError(HTTPException):
    """
    Исключение вызванное не найденым файлом
    """

    pass
