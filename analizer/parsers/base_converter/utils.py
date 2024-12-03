from typing import Any

from parsers.base_converter.exeptions import TypeConvertError


def raise_type_convert_error(value: Any, type_: Any) -> None:
    """
    Вызов исключения TypeConvertError
    """
    raise TypeConvertError(f'Значение {value} не '
                           f'возможно конвертировать в {type_}')
