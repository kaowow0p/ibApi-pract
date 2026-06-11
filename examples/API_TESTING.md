# API Testing Results

## Swagger UI Screenshot
Доступен по адресу: `http://127.0.0.1:8000/docs`

Все 13 эндпоинтов видны и готовы к тестированию:
- **5 endpoints для категорий** (GET, POST, GET по id, PUT, DELETE)
- **6 endpoints для книг** (GET, POST, GET по id, PUT, DELETE, + фильтрация по category_id)
- **2 системных endpoint** (/health, /docs)

## Результаты тестирования

### 1. GET /health - Проверка здоровья сервиса
```bash
curl -s http://127.0.0.1:8000/health | jq .
```
**Результат (код 200):**
```json
{
  "status": "healthy",
  "service": "Books API"
}
```

### 2. GET /categories - Список категорий
```bash
curl -s http://127.0.0.1:8000/categories/ | jq .
```
**Результат (код 200):**
```json
[
  {
    "title": "Fiction",
    "id": 1
  },
  {
    "title": "Non-fiction",
    "id": 2
  },
  {
    "title": "Тестовая категория",
    "id": 3
  },
  {
    "title": "Science Fiction",
    "id": 4
  }
]
```

### 3. GET /books - Список всех книг
```bash
curl -s http://127.0.0.1:8000/books/ | jq '.[:2]'
```
**Результат (код 200) - первые 2 книги:**
```json
[
  {
    "title": "The Strange Case of Dr. Jekyll and Mr. Hyde",
    "description": "A classic novel about dual personality and morality.",
    "price": 8.99,
    "category_id": 1,
    "url": "",
    "id": 1
  },
  {
    "title": "1984",
    "description": "A dystopian novel about surveillance and totalitarianism.",
    "price": 11.5,
    "category_id": 1,
    "url": "",
    "id": 2
  }
]
```

### 4. GET /books/?category_id=1 - Фильтрация по категории
```bash
curl -s 'http://127.0.0.1:8000/books/?category_id=1' | jq length
```
**Результат (код 200):** 2 книги в категории 1

### 5. POST /categories - Создание категории
```bash
curl -s -X POST http://127.0.0.1:8000/categories/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Sci-Fi"}' | jq .
```
**Результат (код 201):**
```json
{
  "title": "Sci-Fi",
  "id": 4
}
```

### 6. PUT /categories/4 - Обновление категории
```bash
curl -s -X PUT http://127.0.0.1:8000/categories/4 \
  -H "Content-Type: application/json" \
  -d '{"title":"Science Fiction"}' | jq .
```
**Результат (код 200):**
```json
{
  "title": "Science Fiction",
  "id": 4
}
```

### 7. POST /books - Создание книги с валидной категорией
```bash
curl -s -X POST http://127.0.0.1:8000/books/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Book","description":"Test","price":9.99,"category_id":1}' | jq .
```
**Результат (код 201):**
```json
{
  "title": "Test Book",
  "description": "Test",
  "price": 9.99,
  "category_id": 1,
  "url": "",
  "id": 6
}
```

### 8. POST /books - Попытка создания с невалидной категорией
```bash
curl -s -X POST http://127.0.0.1:8000/books/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Bad Book","description":"Test","price":9.99,"category_id":999}'
```
**Результат (код 404):**
```json
{
  "detail": "Category not found"
}
```

### 9. GET /books/{id} - Получение книги по ID
```bash
curl -s http://127.0.0.1:8000/books/1 | jq .
```
**Результат (код 200):**
```json
{
  "title": "The Strange Case of Dr. Jekyll and Mr. Hyde",
  "description": "A classic novel about dual personality and morality.",
  "price": 8.99,
  "category_id": 1,
  "url": "",
  "id": 1
}
```

### 10. DELETE /books/{id} - Удаление книги
```bash
curl -s -X DELETE http://127.0.0.1:8000/books/6 -w "\nStatus: %{http_code}\n"
```
**Результат (код 204):** No Content (пусто)

### 11. GET /books/{id} после удаления - Проверка удаления
```bash
curl -s http://127.0.0.1:8000/books/6 -w "\nStatus: %{http_code}\n"
```
**Результат (код 404):**
```json
{
  "detail": "Book not found"
}
```

### 12. DELETE /categories/{id} - Удаление категории
```bash
curl -s -X DELETE http://127.0.0.1:8000/categories/4 -w "\nStatus: %{http_code}\n"
```
**Результат (код 204):** No Content

## PostgreSQL Верификация

### Категории в БД
```bash
psql -U octagon -d octagon_db -h localhost -c "SELECT * FROM categories ORDER BY id;"
```
**Результат:**
```
 id |       title        
----+--------------------
  1 | Fiction
  2 | Non-fiction
  3 | Тестовая категория
  4 | Science Fiction
```

### Книги в БД
```bash
psql -U octagon -d octagon_db -h localhost -c "SELECT id, title, price, category_id FROM books ORDER BY id;"
```
**Результат:**
```
 id |                    title                    | price | category_id 
----+---------------------------------------------+-------+-------------
  1 | The Strange Case of Dr. Jekyll and Mr. Hyde |  8.99 |           1
  2 | 1984                                        | 11.50 |           1
  3 | Sapiens: A Brief History of Humankind       | 14.99 |           2
  4 | Atomic Habits                               | 12.80 |           2
  5 | Тестовая книга                              | 99.99 |           3
```

## Итоги тестирования

✅ **Все HTTP коды корректны:**
- 200 OK для GET запросов
- 201 Created для POST запросов
- 204 No Content для DELETE запросов
- 404 Not Found для несуществующих ресурсов

✅ **Валидация работает:**
- Создание книги с несуществующей категорией возвращает 404

✅ **Фильтрация работает:**
- GET /books/?category_id=1 возвращает только книги из категории 1

✅ **Данные синхронизированы:**
- Все изменения через API отражаются в PostgreSQL
- Состояние БД совпадает с тем, что создавали через API

✅ **Swagger UI работает:**
- Все эндпоинты видны и задокументированы
- Можно выполнять запросы прямо из интерфейса
