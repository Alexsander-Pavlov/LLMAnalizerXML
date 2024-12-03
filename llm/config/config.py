from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel
from starlette.config import Config


base_dir = Path(__file__).resolve().parent.parent
log_dir = base_dir.joinpath('logs')
cache_dir_model = base_dir.joinpath('llm_analizer', 'qwen')


config = Config('.env')


class QWEN2Settings(BaseModel):
    """
    Настройки QWEN2 LLM модели
    """
    NAME: str = 'Qwen/Qwen2.5-1.5B-Instruct'
    MAX_TOKENS: int = 512
    CACHE_DIR: Path = cache_dir_model.absolute()


class LLMSettings(BaseModel):
    """
    Настройки LLM моделей
    """
    QWEN2: QWEN2Settings = QWEN2Settings()
    MODEL: str = 'Qwen/Qwen2.5-1.5B-Instruct'
    TORCH_DTYPE: str = config('TORCH_DTYPE')
    DEVICE_MAP: str = config('DEVICE_MAP')
    REVISION: str = config('REVISION')


class Settings(BaseSettings):
    """
    Настройки проекта
    """
    model_config = SettingsConfigDict(
        extra='ignore',
    )
    LLM: LLMSettings = LLMSettings()
    API_PREFIX: str = '/api/v1'
    BASE_DIR: Path = base_dir
    LOG_DIR: Path = log_dir
    CURRENT_ORIGIN: str = config('CURRENT_ORIGIN')
    ANALIZER_ORIGIN: str = config('ANALIZER_ORIGIN')


settings = Settings()
