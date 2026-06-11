# Examples - Примеры использования Books API

Этот директорий содержит примеры работы с Books API, скриншоты Swagger UI и примеры запросов.

## Быстрый старт

### 1. Запустить FastAPI сервер

```bash
cd /home/kaioshi/Documents/stupidThinks

# Активировать виртуальное окружение
source venv/bin/activate

# Запустить сервер с автоперезагрузкой
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Сервер будет доступен на: **http://127.0.0.1:8000**

### 2. Открыть Swagger UI

Перейти в браузер на: **http://127.0.0.1:8000/docs**

Здесь вы сможете:
- Увидеть все 13 эндпоинтов API
- Просмотреть полную документацию каждого эндпоинта
- Выполнить тестовые запросы прямо из интерфейса

### 3. Проверить здоровье API

```bash
curl -s http://127.0.0.1:8000/health | jq .
```

## Примеры curl команд

### Получить все категории
```bash
curl -s http://127.0.0.1:8000/categories/ | jq .
```

### Получить все книги
```bash
curl -s http://127.0.0.1:8000/books/ | jq .
```

### Получить книги из категории 1
```bash
curl -s 'http://127.0.0.1:8000/books/?category_id=1' | jq .
```

### Создать категорию
```bash
curl -X POST http://127.0.0.1:8000/categories/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Новая категория"}' | jq .
```

### Создать книгу
```bash
curl -X POST http://127.0.0.1:8000/books/ \
  -H "Content-Type: application/json" \
  -d '{
    "title":"Название книги",
    "description":"Описание",
    "price":19.99,
    "category_id":1
  }' | jq .
```

### Обновить категорию
```bash
curl -X PUT http://127.0.0.1:8000/categories/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"Обновленное название"}' | jq .
```

### Удалить книгу
```bash
curl -X DELETE http://127.0.0.1:8000/books/1
```

## Проверка PostgreSQL

Убедиться, что данные сохранились в БД:

```bash
# Подключиться к БД
psql -U octagon -d octagon_db -h localhost

# Просмотреть категории
SELECT * FROM categories;

# Просмотреть книги
SELECT * FROM books;

# Выход
\q
```

## API Endpoints

### Categories (Категории)
- `GET /categories/` - Список всех категорий
- `GET /categories/{category_id}` - Получить категорию по ID
- `POST /categories/` - Создать новую категорию
- `PUT /categories/{category_id}` - Обновить категорию
- `DELETE /categories/{category_id}` - Удалить категорию

### Books (Книги)
- `GET /books/` - Список всех книг (с опциональным фильтром ?category_id=)
- `GET /books/{book_id}` - Получить книгу по ID
- `POST /books/` - Создать новую книгу
- `PUT /books/{book_id}` - Обновить книгу
- `DELETE /books/{book_id}` - Удалить книгу

### System (Система)
- `GET /` - Информация об API
- `GET /health` - Проверка здоровья сервиса

## HTTP Коды ответов

| Код | Значение | Когда используется |
|-----|----------|-------------------|
| **200** | OK | GET запросы, успешные PUT |
| **201** | Created | Успешное создание ресурса (POST) |
| **204** | No Content | Успешное удаление (DELETE) |
| **404** | Not Found | Ресурс не найден |
| **400** | Bad Request | Ошибка валидации данных |

## Документация

- [API_TESTING.md](./API_TESTING.md) - Подробные результаты тестирования всех эндпоинтов

## Требования

- Python 3.10+
- PostgreSQL 12+
- FastAPI 0.136.3
- SQLAlchemy 2.0.50
- Uvicorn 0.49.0

Все зависимости указаны в `requirements.txt`
