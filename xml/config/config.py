from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel
from starlette.config import Config


base_dir = Path(__file__).resolve().parent.parent
log_dir = base_dir.joinpath('logs')


config = Config('.env')


class Regex(BaseModel):
    """
    Регулярные выражения
    """
    XML_REGEX: str = r'^\w+\.xml$'


class Settings(BaseSettings):
    """
    Настройки проекта
    """
    model_config = SettingsConfigDict(
        extra='ignore',
    )
    API_PREFIX: str = '/api/v1'
    BASE_DIR: Path = base_dir
    LOG_DIR: Path = log_dir
    CURRENT_ORIGIN: str = config('CURRENT_ORIGIN')
    ANALIZER_ORIGIN: str = config('ANALIZER_ORIGIN')
    regex: Regex = Regex()
    NAME_XML: str = 'items.xml'
    PATH_ITEMS_XML: Path = BASE_DIR.joinpath(NAME_XML)


settings = Settings()
