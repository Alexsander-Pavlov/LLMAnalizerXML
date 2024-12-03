from pathlib import Path
from transformers import (
    AutoTokenizer,
    PreTrainedModel,
    AutoModelForCausalLM,
    PreTrainedTokenizer,
    PreTrainedTokenizerFast,
    )
from typing import ClassVar

from config import settings


class Qwen2LLM:
    """
    Класс LLM модели Qwen2.
    Данная модель предназначена для аналитики данных.

    ## Предназначение:

    Основное назначение этого класса это:
    - Загрузка LLM модели локально.
    - Настройка.
    - Составление запроса.
    - Обработка запроса LLM моделью.

    ## Методы:
    - :class:`Qwen2LLM.load_model()` - загрузка модели локально\
        в кэш.
    - :class:`Qwen2LLM.get_model_name_cache()` - вывод имени модели\
        которое будет использоваться для загрузки.
    - :class:`Qwen2LLM.get_locks_dir()` - вывод пути к папке модели\
        которое будет использоваться для `.locks`.
    - :class:`Qwen2LLM.get_cache_model_dir()` - вывод пути к папке\
        которая будет использоваться для загрузки модели.
    - :class:`Qwen2LLM.send_answer(answer)` - запрос к LLM модели\
        для обрабоки данных.

    ## Примеры:
    ```python
    question = [
        {
            'role': 'system',
            'content': 'You are analyzer',
        },
        {
            'role': 'user',
            'content': 'Analyze this data, please.',
        },
    ]
    # Отдать запрос LLM модели.
    answer = Qwen2LLM.send_answer(question)
    ```
    """
    model_name: ClassVar[str] = settings.LLM.QWEN2.NAME
    cache_dir: ClassVar[Path] = settings.LLM.QWEN2.CACHE_DIR
    model: ClassVar[PreTrainedModel | None] = None
    torch_dtype: str = settings.LLM.TORCH_DTYPE
    device_map: str = settings.LLM.DEVICE_MAP
    revision: str = settings.LLM.REVISION
    max_tokens: int = settings.LLM.QWEN2.MAX_TOKENS

    @classmethod
    def load_model(cls):
        cls.model = AutoModelForCausalLM.from_pretrained(
            cls.model_name,
            cache_dir=cls.cache_dir,
            torch_dtype=cls.torch_dtype,
            device_map=cls.device_map,
            revision=cls.revision,
        )

    @classmethod
    def _get_tokinazer(cls,
                       model_name: str,
                       ) -> PreTrainedTokenizer | PreTrainedTokenizerFast:
        tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            cache_dir=cls.cache_dir,
            use_fast=True,
        )
        return tokenizer

    @classmethod
    def _apply_chat_tokenizer(cls,
                              tokenizer: (PreTrainedTokenizer |
                                          PreTrainedTokenizerFast),
                              message: list[dict[str, str]],
                              ) -> list[int]:
        return tokenizer.apply_chat_template(
            message,
            tokenize=False,
            add_generation_prompt=True,
        )

    @classmethod
    def _response(cls,
                  tokenizer: (PreTrainedTokenizer |
                              PreTrainedTokenizerFast),
                  model: PreTrainedModel,
                  chat: list[str],
                  ) -> str:
        model_inputs = tokenizer([chat], return_tensors="pt").to(model.device)
        generated_ids = model.generate(
            **model_inputs,
            max_new_tokens=cls.max_tokens,
            )
        generated_ids = [output_ids[len(input_ids):] for
                         input_ids, output_ids in
                         zip(model_inputs.input_ids, generated_ids)]
        return tokenizer.batch_decode(generated_ids, skip_special_tokens=True)

    @classmethod
    def get_model_name_cache(cls) -> str:
        return 'models--' + cls.model_name.replace('/', '--')

    @classmethod
    def get_locks_dir(cls) -> Path:
        return cls.cache_dir.joinpath('.locks')

    @classmethod
    def get_cache_model_dir(cls) -> Path:
        cache_name = cls.get_model_name_cache()
        return cls.cache_dir.joinpath(cache_name)

    @classmethod
    def send_answer(cls, answer: list[dict[str, str]]) -> list[str]:
        if (not cls.get_locks_dir().exists() or
            not cls.get_cache_model_dir().exists() or
            not cls.model
        ):
            cls.load_model()
        tokenizer = cls._get_tokinazer(cls.model_name)
        chat = cls._apply_chat_tokenizer(
            tokenizer=tokenizer,
            message=answer,
        )
        response = cls._response(
            tokenizer=tokenizer,
            model=cls.model,
            chat=chat
        )
        return response


Qwen = Qwen2LLM()
