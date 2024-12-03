from typing import Any, Mapping
from starlette.background import BackgroundTask

from xml.dom import minidom

from fastapi.responses import Response, PlainTextResponse
from api_v1.utils import correct_xml_path


class FileXMLRender(Response):
    """
    Рендер XML ответа

    ## Example
    ``` python
    from fastapi import APIRouter
    from api_v1.renders import FileXMLRender

    router = APIRouter(prefix='/xml',
                    tags=['XML'],
                    )

    @router.get(path='/get-list',
                response_class=FileXMLRender,
                )
    async def get_products_xml():
        return 'some/xml_file.xml'
    ```
    """
    media_type = 'application/xml'
    charset = 'utf-8'

    def __init__(
        self,
        content: Any = None,
        status_code: int = 200,
        headers: Mapping[str, str] | None = None,
        media_type: str | None = None,
        background: BackgroundTask | None = None,
    ) -> None:
        super().__init__(content, status_code, headers, media_type, background)

    def render(self,
               value: Any,
               ) -> PlainTextResponse:
        xml = correct_xml_path(value)
        return minidom.parse(xml.as_posix()).toxml(encoding='utf-8')
