import pathlib
from fastapi import HTTPException, status

from api_v1.regex import check_xml_file
from api_v1.exeptions import ValidationError, APIFileNotFoundError


def correct_xml_path(path: str) -> pathlib.Path:
    """
    Серия проверок для корректности полученого адресса XML

    ## Args:
        path (str): Ссылка на адресс пути

    ## Raises:
        HTTPException: В случае пустого значения <br>
        APIFileNotFoundError: Если файл не найден или по пути
        находится нечто иное <br>

        ValidationError: Если формат файла не XML

    ## Returns:
        pathlib.Path: Возвращает адресс в формате :class:`pathlib.Path`

    ## Example
    ```python
    # Right
    path = 'var/exists_file.xml'
    correct_path = correct_xml_path(path=path)

    # HTTPException: No data
    path = ''
    correct_path = correct_xml_path(path=path)

    # ValidationError: File is not XML
    path = 'var/somefile.txt'
    correct_path = correct_xml_path(path=path)

    # APIFileNotFoundError: Object is not file
    path = 'var/dir'
    correct_path = correct_xml_path(path=path)

    # APIFileNotFoundError: File is not found
    path = 'var/no_exists_file.xml'
    correct_path = correct_xml_path(path=path)
    ```
    """
    if not path:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=dict(file='No data'))
    path = pathlib.Path(str(path))
    if not path.exists():
        raise APIFileNotFoundError(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=dict(file='File is not found'),
            )
    if not path.is_file():
        raise APIFileNotFoundError(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=dict(file='Object is not file'),
            )
    file_ = path.name
    if not check_xml_file(file_):
        raise ValidationError(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=dict(file='File is not XML'),
            )
    return path
