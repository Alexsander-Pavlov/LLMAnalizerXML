# LLM Анализатор для XML файлов на основе выборки
Данный проект реализует множество различных функциональностей.
## Цель
Цель проекта это - парсинг XML документа из определенного энд поинта
по определенному периоду времени, а затем составление Prompt для LLM модели.
После всех действий данные отдаются LLM модели которая в свою очередь 
анализирует данные и отдает ответ - ответ сохраняется в Базу Данных.
## Структура
В Проекте Реализованна микросервисная архитектура
Микросервисы:
 - analizer
 - xml
 - llm
### analizer
Сервис analizer отвечает за обработку XML файлов, а так же
является центральным сервисом который занимается периодическими 
задачами по обработке всех данных и запросов в другие сервисы.
### Реализованные классы
- Парсеры. <br>
    Парсеры неоходимы для парсинга неформальных данных
    и переопределяют данные в необходимую структуру.
    - BaseXMLParser
    - StringXMLParser
    - FileXMLParser

    BaseXMLParser - 
    Базовый класс XML парсера, предназначен только для 
    наследование и реализует базовую функциональность.

    StringXMLParser - 
    Парсер который специализируется на парсинге строковой модели данных
    ```python
    from config import settings
    from parsers import StringXMLParser

    # response ответ от Энд Поинта
    body = response.content.decode(encoding='utf-8')
    parser = StringXMLParser(xml=body,
                             target_items=settings.TARGET_ITEMS_XML,
                             attrs=(settings.TARGET_ATTRS_XML,),
                             )
    # Получение генератора
    parsed_items = parser.get_generator()
    ```

    FileXMLParser
    Парсер который специализируется на парсинге Файла
    ```python
    from config import settings
    from pathlib import Path
    from parsers import FileXMLParser


    path = Path('some_xml_file')

    # Открытие файла
    with path.open(mode='r', encoding='utf-8') as file_:
        parser = FileXMLParser(xml=file_,
                               target_items=settings.TARGET_ITEMS_XML,
                               attrs=(settings.TARGET_ATTRS_XML,),
                               )
    # Получение генератора
    parsed_items = parser.get_generator()
    ```
- Конверторы типов. <br>
    Конверторы типов играют важную роль в фазе парсинга,
    они обеспечивают нужный тип данных для дальнейшей обработке
    на протяжении всего парсинга.
    - BaseTypeConverter
    - DefaultTypeConverter

    BaseTypeConverter - 
    Базовый конвертор предназначен только для наследования,
    реализует базовый функционал.

    DefaultTypeConverter - 
    "Дэфолтный" конвертор который стандартным образом
    обеспечивает конвертацию данных.

    ```python
    from config import settings
    from parsers import StringXMLParser
    from parsers.type_converters import DefaultTypeConverter

    # response ответ от Энд Поинта
    body = response.content.decode(encoding='utf-8')
    parser = StringXMLParser(xml=body,
                             target_items=settings.TARGET_ITEMS_XML,
                             attrs=(settings.TARGET_ATTRS_XML,),
                             type_converter=DefaultTypeConverter,
                             convert_int=True,
                             convert_float=True,
                             convert_date=True,
                             )
    # Получение генератора
    parsed_items = parser.get_generator()
    ```
- Создатель Промптов. <br>
    Этот важный класс отвечает за правильную и надежную
    генерацию запроса для LLM.
    - ProductPromptMaker

    ProductPromptMaker
    Генерирует Промпт для LLM модели

    ```python
    from datetime import date
    from task_schedule.utils import ProductPromptMaker


    date = date(2024, 1, 1)
    session = AsyncSession
    prompt_maker = ProductPromptMaker(
        session=session,
        date=date
    )
    prompt = await prompt_maker.get_prompt()
    ```
### xml
XML сервис предназначен только как энд поинт для выдачи XML файла.
### Реализованные классы и функции
- Рендеры
    - FileXMLRender. <br>
    FileXMLRender нужен для корректного ответа от Энд Поинта
    в виде XML, в нем завязана логика проверки файлов и формата.

    ```python
    from fastapi import APIRouter

    from api_v1.renders import FileXMLRender

    from config import settings


    router = APIRouter(prefix='/xml',
                       tags=['XML'],
                       )


    @router.get(path='/get-list',
                description='Get list of Products (XML)',
                name='Products XML',
                response_class=FileXMLRender, # Указание типа рендера
                )
    async def get_products_xml():
        return settings.PATH_ITEMS_XML.as_posix() # Адресс на XML файл
    ```

    - correct_xml_path. <br>
    correct_xml_path проводит серию проверок полученного адресса XML файла.

    ```python
    from pathlib import Path


    path = Path('some_xml_file.xml')
    correct_path = correct_xml_path(path)
    ```
### LLM
LLM сервис предназначен для обработки входных данных LLM моделью.
### Реализованные классы
- LLM
    - Qwen2LLM. <br>
    Qwen2LLM предназначен для загрузки Qwen2 LLM модели,
    а так же сбора prompt и обращении к самой модели.
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
## Запуск
### Окружение переменных
Имеются несколько окружений:
1. Общее - в корне проекта
2. analizer
3. llm
4. xml
В каждом из окружений имеется `env.sample` - переменуйте в `.env`
### Docker
Проект находится под системой управления и контеризации - **Docker**.
Если у вас нет Docker - вы можете установить его с официального сайта: [Docker](https://www.docker.com/get-started/)
- Cделайте "Билд"
```bash
docker compose build
```
- Затем запустите окружение
```bash
docker compose up
```
После успешного запуска приложение будет доступно по адрессам:
- analizer: http://localhost:8080
- llm: http://localhost:8081
- xml: http://localhost:8082
- Grafana: http://localhost:3000
- Flower: http://localhost:5555
## Как пользоваться
После запуска проекта - работа в основном в фоне.
- Вы можете перейти на http://localhost:8080/docs/, и там будут 
два энд поинта.
    - api/v1/products/get-list: Отвечает за вывод всех полученных продуктов.
    - api/v1/answers/list: Отвечает за вывод всех ответов за даты.
- Так же на http://localhost:8081
    - api/v1/llm/analyst-manager: Отвечает за запросы к LLM модели.
- И http://localhost:8082
    - api/v1/xml/get-list: Отвечает за выдачу XML файла для обработки.<br>

Есть таймер который раз в сутки в 2:00 AM - запускает задачу для анализа данных
полученных из http://localhost:8082/api/v1/xml/get-list, и анализует данные.
Предпологается что данные каждые сутки обновляются (предпологается статистика продаж магазина за день).
## Как это работает?
Когда таймер срабатывает - запускается задача.
### Задача
Задача вмещает в себя весь необходимый алгоритм по обработке всех Данных:
- Получение XML из http://localhost:8082/api/v1/xml/get-list;
- Парсинг полученных данных с помощью %%StringXMLParser%%;
    - Конвертация типов из строчного формата в логический (опционально - можно настроить);
    - Составление необходимой структуры данных из полученных данных;
    - Вывод генератора (для оптимизации);
- Сохранение данных в базу данных (одним коммитом);
- Составление запроса для LLM с помощью %%ProductPromptMaker%%;
    - Выборка 3 лучших продуктов по продажам за период;
    - Выборка общей выручки за период;
    - Выборка действуйщих категорий за период;
    - Составление запроса по шаблону для LLM модели;
- Обращение к LLM по энд поинту http://localhost:8081
    - Получение данных;
    - Получение предварительно загруженой в локальный кэш модели;
    - Получение токенайзера;
    - Конветация запроса в последовательсть ID (формат для LLM);
    - Обращение к LLM модели и передача запроса;
    - Получение ответа;
    - Отдать ответ обратно адрессату;
- Получение ответа от LLM модели;
- Сохранение ответа в Базу Данных;
## Инструменты
## RabbitMQ, Celery
Используется Брокер сообщений RabbitMQ и Worker Celery
### Docker RabbitMQ
```yaml
rabbitmq:
    hostname: rabbitmq
    image: rabbitmq:4.0.3-management
    env_file:
      - .env
    ports:
      - 5672:5672
      - 15672:15672
    volumes:
      - rabbitmq-data:/var/lib/rabbitmq

volumes:
  rabbitmq-data:
```

### Настройка RabbitMQ
```python
# .env
RABBITMQ_DEFAULT_USER=guest # Логин RabbitMQ
RABBITMQ_DEFAULT_PASS=guest # Пароль RabbitMQ
```
### Docker Celery Worker
```yaml
celery_worker:
    build: 
      context: .
      dockerfile: ./docker/fastapi/Dockerfile
    command: /start-celeryworker
    volumes:
      - .:/app
    env_file:
      - .env
```

### Настройка Celery
```python
# congin/rabbitmq/connection.py
from config.config import settings


app = Celery(__name__)
app.conf.broker_url = settings.rabbit.broker_url
app.autodiscover_tasks(packages=['project.packages'])
```
### Класс Celery
Есть реализация Асихронного класса Celery
для выполнения задач в асинхронном режиме.

### Использование
После настройки RabbitMQ и Celery
Вам необходимо запустить проект (инструкции ниже)
а затем перейти по адрессу:
http://localhost:15672/
Это будет страница RabbitMQ для просмотра всех каналов, очередей,
обмеников, пользователей, и.т.д.
Вам нужно будет ввести логин и пароль для аутентификации который вы указали в .env

## Flower
Flower это мощное приложение для отслеживания всех
задач на стороне Worker.
### Docker Flower
```yaml
dashboard:
    build: 
      context: .
      dockerfile: ./docker/fastapi/Dockerfile
    command: /start-flower
    volumes:
      - .:/app
    ports:
      - 5555:5555
    env_file:
      - .env
```

### Настройка
Предварительная настройка не требуется, все настройки подтягиваются
автоматически из RabbitMQ.

### Использование
Для использования Flower вам нужно перейти по адрессу:
http://localhost:5555/
У вас откроется страница Flower с полной информацией о Worker и Tasks.
## SQLAlchemy
SQLAlchemy используется асинхронный.
Реализованн специальный класс для поддежки подключения и 
делегированнием сессий.
- DataBaseHelper

```python
# Инициализация соединения с Базой Данных на текущий HTTP запрос
async with db_helper.engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)
    yield # Событие HTTP запроса
await db_helper.dispose()

# "Протаскивание" текущей сессии для запросов к Базе данных на этот HTTP запрос
async def get_session(session: AsyncSession = Depends(db_helper.session_geter)):
    current_session = session
    return session
```
# OpenAI
FastAPI поддерживает автоматическую генерацию документации и взаимодействие с API.
Для более легкого просмотра возможностей проекта (пока нет клиента) вы можете прейти по ссылке:
http://localhost:8080/docs/
http://localhost:8081/docs/
http://localhost:8082/docs/
