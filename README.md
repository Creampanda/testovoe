# Meme API Service
## Описание
Meme API Service - это веб-приложение, разработанное с использованием FastAPI, которое предоставляет API для работы с коллекцией мемов. Приложение состоит из публичного API с бизнес-логикой и сервиса для работы с медиа-файлами, используя S3-совместимое хранилище (например, MinIO).

### Функциональность

### Public API
GET /memes: Получить список всех мемов (с пагинацией).

### Internal API
GET /memes/{id}: Получить конкретный мем по его ID.

POST /memes: Добавить новый мем (с картинкой и текстом).

PUT /memes/{id}: Обновить существующий мем.

DELETE /memes/{id}: Удалить мем.

### Требования
- Docker
- Docker Compose

## Установка и запуск
Клонируйте репозиторий:

```bash
git clone https://github.com/Creampanda/testovoe
cd meme-api-service
```
Запустите сервисы с помощью Docker Compose:

```bash
docker-compose up --build
```

Добавьте MinIO в файл /etc/hosts:

Откройте файл /etc/hosts и добавьте следующую строку:

```bash
127.0.0.1        minio
```

## Документация API:

- Публичный API: http://localhost:8000/docs
- Внутренний API: http://localhost:8001/docs

## Структура проекта
- api_service/: Основной код сервиса API.
- db/: SQL-скрипты для инициализации базы данных.
- docker-compose.yml: Файл конфигурации Docker Compose для запуска всех сервисов.
- Dockerfile: Файл Docker для сборки образа API сервиса.
- requirements.txt: Файл зависимостей Python.

## Тестирование
Для тестирования основного функционала были написаны несколько unit-тестов. Вы можете запустить тесты с использованием pytest:
```bash
git clone https://github.com/Creampanda/testovoe
cd testovoe
```
Создать и запустить virtual environment
```bash
python3 -m venv env
source env/bin/activate
```
Установить зависимости
```bash
pip3 install -r api_service/requirements.txt 
```
Запустить тесты
```bash
pytest
```
# Заключение
Этот проект демонстрирует создание API сервиса для работы с мемами с использованием FastAPI и MinIO для хранения медиа-файлов. Следуя инструкциям в этом README, вы сможете развернуть и протестировать сервис локально.

Если у вас возникнут вопросы или проблемы, пожалуйста, обратитесь к документации FastAPI и MinIO, или создайте issue в репозитории проекта.