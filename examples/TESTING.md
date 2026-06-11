# Testing Guide - Books API

Полная инструкция по тестированию API с примерами запросов.

## 🎯 Быстрый старт

1. **Запустить сервер:**
   ```bash
   . venv/bin/activate
   python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```

2. **Открыть Swagger UI:**
   ```
   http://127.0.0.1:8000/docs
   ```

3. **Проверить здоровье:**
   ```bash
   curl http://127.0.0.1:8000/health
   ```

## 📊 Примеры curl запросов

### Health Check

```bash
curl http://127.0.0.1:8000/health
```

**Ответ (200 OK):**
```json
{"status": "healthy", "service": "Books API"}
```

### Category Operations

#### 1. Получить все категории
```bash
curl http://127.0.0.1:8000/categories/
```

**Ответ (200 OK):**
```json
[
  {"title": "Fiction", "id": 1},
  {"title": "Non-fiction", "id": 2},
  {"title": "Тестовая категория", "id": 3}
]
```

#### 2. Получить категорию по ID
```bash
curl http://127.0.0.1:8000/categories/1
```

**Ответ (200 OK):**
```json
{"title": "Fiction", "id": 1}
```

#### 3. Создать новую категорию
```bash
curl -X POST http://127.0.0.1:8000/categories/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Science Fiction"}'
```

**Ответ (201 Created):**
```json
{"title": "Science Fiction", "id": 4}
```

#### 4. Обновить категорию
```bash
curl -X PUT http://127.0.0.1:8000/categories/4 \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Science Fiction"}'
```

**Ответ (200 OK):**
```json
{"title": "Updated Science Fiction", "id": 4}
```

#### 5. Удалить категорию
```bash
curl -X DELETE http://127.0.0.1:8000/categories/4
```

**Ответ (204 No Content):**
```
(пустой ответ, только статус код)
```

### Book Operations

#### 1. Получить все книги
```bash
curl http://127.0.0.1:8000/books/
```

**Ответ (200 OK):**
```json
[
  {
    "title": "1984",
    "description": "A dystopian novel...",
    "price": 11.5,
    "category_id": 1,
    "url": "",
    "id": 2
  },
  ...
]
```

#### 2. Фильтрация книг по категории
```bash
curl "http://127.0.0.1:8000/books/?category_id=1"
```

**Ответ (200 OK):**
```json
[
  {
    "title": "The Strange Case of Dr. Jekyll and Mr. Hyde",
    "description": "A classic novel...",
    "price": 8.99,
    "category_id": 1,
    "url": "",
    "id": 1
  },
  {
    "title": "1984",
    "description": "A dystopian novel...",
    "price": 11.5,
    "category_id": 1,
    "url": "",
    "id": 2
  }
]
```

#### 3. Получить книгу по ID
```bash
curl http://127.0.0.1:8000/books/1
```

**Ответ (200 OK):**
```json
{
  "title": "The Strange Case of Dr. Jekyll and Mr. Hyde",
  "description": "A classic novel...",
  "price": 8.99,
  "category_id": 1,
  "url": "",
  "id": 1
}
```

#### 4. Создать новую книгу
```bash
curl -X POST http://127.0.0.1:8000/books/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Hobbit",
    "description": "A fantasy novel",
    "price": 15.99,
    "category_id": 1,
    "url": "https://en.wikipedia.org/wiki/The_Hobbit"
  }'
```

**Ответ (201 Created):**
```json
{
  "title": "The Hobbit",
  "description": "A fantasy novel",
  "price": 15.99,
  "category_id": 1,
  "url": "https://en.wikipedia.org/wiki/The_Hobbit",
  "id": 6
}
```

#### 5. Обновить книгу
```bash
curl -X PUT http://127.0.0.1:8000/books/6 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Hobbit: Updated",
    "price": 16.99
  }'
```

**Ответ (200 OK):**
```json
{
  "title": "The Hobbit: Updated",
  "description": "A fantasy novel",
  "price": 16.99,
  "category_id": 1,
  "url": "https://en.wikipedia.org/wiki/The_Hobbit",
  "id": 6
}
```

#### 6. Удалить книгу
```bash
curl -X DELETE http://127.0.0.1:8000/books/6
```

**Ответ (204 No Content):**
```
(пустой ответ, только статус код)
```

## ✋ Ошибки и обработка

### 404 Not Found
```bash
curl http://127.0.0.1:8000/categories/999
```

**Ответ (404):**
```json
{"detail": "Category not found"}
```

### 404 при создании книги с несуществующей категорией
```bash
curl -X POST http://127.0.0.1:8000/books/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Book",
    "price": 20.0,
    "category_id": 999
  }'
```

**Ответ (404):**
```json
{"detail": "Category not found"}
```

## 🧪 Интеграционное тестирование

### Полный цикл CRUD

```bash
#!/bin/bash

# 1. Создать категорию
CATEGORY=$(curl -s -X POST http://127.0.0.1:8000/categories/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Category"}')

CATEGORY_ID=$(echo $CATEGORY | jq '.id')
echo "✓ Created category with ID: $CATEGORY_ID"

# 2. Создать книгу в этой категории
BOOK=$(curl -s -X POST http://127.0.0.1:8000/books/ \
  -H "Content-Type: application/json" \
  -d "{
    \"title\": \"Test Book\",
    \"description\": \"Test Description\",
    \"price\": 29.99,
    \"category_id\": $CATEGORY_ID,
    \"url\": \"https://test.com\"
  }")

BOOK_ID=$(echo $BOOK | jq '.id')
echo "✓ Created book with ID: $BOOK_ID"

# 3. Получить книги в категории
curl -s "http://127.0.0.1:8000/books/?category_id=$CATEGORY_ID" | jq .
echo "✓ Listed books in category"

# 4. Обновить книгу
curl -s -X PUT http://127.0.0.1:8000/books/$BOOK_ID \
  -H "Content-Type: application/json" \
  -d '{"price": 39.99}' | jq .
echo "✓ Updated book price"

# 5. Удалить книгу
curl -s -X DELETE http://127.0.0.1:8000/books/$BOOK_ID
echo "✓ Deleted book"

# 6. Удалить категорию
curl -s -X DELETE http://127.0.0.1:8000/categories/$CATEGORY_ID
echo "✓ Deleted category"
```

## 📝 Верификация PostgreSQL

```bash
# Подключиться к БД
PGPASSWORD=12345 psql -U octagon -d octagon_db -h localhost

# В psql выполнить:
SELECT * FROM categories;
SELECT * FROM books;

# Или через одну команду:
PGPASSWORD=12345 psql -U octagon -d octagon_db -h localhost \
  -c "SELECT * FROM categories; SELECT * FROM books;"
```

## 🎬 Скриншоты примеров

В папке `examples/` находятся:

1. **Swagger UI** - интерактивная документация API
2. **API Response примеры** - JSON ответы от API
3. **PostgreSQL данные** - результаты SELECT запросов

## ✅ Чек-лист тестирования

- [ ] Swagger UI доступен на /docs
- [ ] Health check возвращает 200
- [ ] GET /categories/ возвращает список категорий
- [ ] POST /categories/ создает новую категорию (201)
- [ ] GET /categories/{id} возвращает категорию (200)
- [ ] PUT /categories/{id} обновляет категорию (200)
- [ ] DELETE /categories/{id} удаляет категорию (204)
- [ ] GET /books/ возвращает список книг
- [ ] GET /books/?category_id=1 фильтрует по категории
- [ ] POST /books/ создает новую книгу (201)
- [ ] GET /books/{id} возвращает книгу (200)
- [ ] PUT /books/{id} обновляет книгу (200)
- [ ] DELETE /books/{id} удаляет книгу (204)
- [ ] 404 ошибки корректно обрабатываются
- [ ] Валидация категории при создании книги работает
- [ ] Данные синхронизированы между API и PostgreSQL

## 🔍 Отладка

### Просмотр логов Uvicorn
Логи выводятся где запущен `uvicorn`:
```
INFO:     127.0.0.1:xxxxx - "GET /books/ HTTP/1.1" 200 OK
```

### Включить дополнительный logging
```bash
python -m uvicorn app.main:app --reload --log-level debug
```

### Проверить подключение к БД
```bash
PGPASSWORD=12345 psql -U octagon -d octagon_db -h localhost -c "SELECT 1"
```
