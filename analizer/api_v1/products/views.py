from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import ProductSchema
from .dao import ProductDAO
from config import db_connection


router = APIRouter(prefix='/products',
                   tags=['Products'],
                   )


@router.get(path='/list')
async def get_list_products(
    session: AsyncSession = Depends(db_connection.session_geter)
) -> list[ProductSchema]:
    return await ProductDAO.find_all_items_by_args(
        session=session,
    )
