from fastapi import APIRouter

from llm_analizer import Qwen
from .schemas import GetDataAnalystSchema


router = APIRouter(prefix='/llm',
                   tags=['LLM'],
                   )


@router.put(path='/analyst-manager',
            description='Send Prompt to Analyst',
            name='Request to Analyst',
            )
async def request_analys(message: list[GetDataAnalystSchema]) -> list[str]:
    analyst = Qwen
    response = analyst.send_answer(message)
    return response
