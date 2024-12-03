from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config import db_connection
from .schemas import AnswerSchema
from .dao import AnswerDAO


router = APIRouter(prefix='/answers',
                   tags=['Answers'],
                   )


@router.get(path='/list')
async def get_list_answers(
    session: AsyncSession = Depends(db_connection.session_geter),
) -> list[AnswerSchema]:
    return await AnswerDAO.find_all_items_by_args(
        session=session,
    )
