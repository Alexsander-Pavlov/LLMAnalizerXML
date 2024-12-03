from collections.abc import MutableMapping
from datetime import date

from parsers.base_converter import BaseTypeConverter
from parsers.base_converter.exeptions import TypeConvertError


class DefaultTypeConverter(BaseTypeConverter):
    """
    Конвертер типов по умолчанию.

    Неоходим для стандартного объема задач.

    ## Пример:
    ```python
    dict_ = dict(
        name='some_name',
        date='2020-11-1'
        price='3300.11,
        quantity='4',
    )
    converter = DefaultTypeConverter(value=dict_)
    converted_dict = converter.convert()
    converted_dict
    <<
    {
        name: 'some_name',
        date=date(2020, 11, 1),
        price=3300.11,
        quantity=4,
    }
    >>
    ```
    """

    def _convert_types(self,
                       value: str,
                       parse_int: bool,
                       parse_float: bool,
                       parse_date: bool,
                       ) -> int | float | date:
        try:
            if parse_int:
                if value.isdigit():
                    try:
                        value = self.convert_int(value)
                        return value
                    except TypeConvertError:
                        pass
            if parse_float:
                try:
                    self.convert_int(value)
                except TypeConvertError:
                    try:
                        value = self.convert_float(value)
                        return value
                    except TypeConvertError:
                        pass
            if parse_date:
                if value.find('-') != -1:
                    check = value.replace('-', '')
                    if len(check) == 8 and check.isdigit():
                        value = self.convert_date(value)
                        return value
        except AttributeError:
            pass
        return value

    def convert(self) -> MutableMapping:
        for values in self:
            self[values[0]] = self._convert_types(
                value=values[-1],
                parse_int=self.parse_int,
                parse_float=self.parse_float,
                parse_date=self.parse_date,
            )
        return self.contaiter
