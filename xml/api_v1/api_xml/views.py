from fastapi import APIRouter

from api_v1.renders import FileXMLRender

from config import settings


router = APIRouter(prefix='/xml',
                   tags=['XML'],
                   )


@router.get(path='/get-list',
            description='Get list of Products (XML)',
            name='Products XML',
            response_class=FileXMLRender,
            )
async def get_products_xml():
    return settings.PATH_ITEMS_XML.as_posix()
