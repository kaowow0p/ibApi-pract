#!/bin/bash
# Примеры curl команд для тестирования Books API

# Убедитесь, что сервер запущен:
# python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

API_URL="http://127.0.0.1:8000"

echo "=== 1. Проверка здоровья API ==="
curl -s "$API_URL/health" | jq .
echo

echo "=== 2. Получить все категории ==="
curl -s "$API_URL/categories/" | jq .
echo

echo "=== 3. Получить одну категорию по ID ==="
curl -s "$API_URL/categories/1" | jq .
echo

echo "=== 4. Получить все книги ==="
curl -s "$API_URL/books/" | jq .
echo

echo "=== 5. Получить книги из категории 1 ==="
curl -s "$API_URL/books/?category_id=1" | jq .
echo

echo "=== 6. Получить одну книгу по ID ==="
curl -s "$API_URL/books/1" | jq .
echo

echo "=== 7. Создать новую категорию (POST, ожидаем 201) ==="
curl -s -X POST "$API_URL/categories/" \
  -H "Content-Type: application/json" \
  -d '{"title":"Создана через curl"}' \
  -w "\nStatus: %{http_code}\n" | jq .
echo

echo "=== 8. Создать новую книгу с валидной категорией (POST, ожидаем 201) ==="
curl -s -X POST "$API_URL/books/" \
  -H "Content-Type: application/json" \
  -d '{
    "title":"Новая книга",
    "description":"Создана через curl",
    "price":29.99,
    "category_id":1
  }' \
  -w "\nStatus: %{http_code}\n" | jq .
echo

echo "=== 9. Попытка создать книгу с несуществующей категорией (ожидаем 404) ==="
curl -s -X POST "$API_URL/books/" \
  -H "Content-Type: application/json" \
  -d '{
    "title":"Плохая книга",
    "description":"Invalid category",
    "price":9.99,
    "category_id":999
  }' \
  -w "\nStatus: %{http_code}\n"
echo

echo "=== 10. Обновить категорию (PUT, ожидаем 200) ==="
curl -s -X PUT "$API_URL/categories/1" \
  -H "Content-Type: application/json" \
  -d '{"title":"Fiction (Обновлено)"}' \
  -w "\nStatus: %{http_code}\n" | jq .
echo

echo "=== 11. Удалить книгу (DELETE, ожидаем 204) ==="
curl -s -X DELETE "$API_URL/books/1" \
  -w "\nStatus: %{http_code}\n"
echo

echo "=== 12. Убедиться что книга удалена (ожидаем 404) ==="
curl -s "$API_URL/books/1" \
  -w "\nStatus: %{http_code}\n"
echo

echo "=== 13. Открыть Swagger UI ==="
echo "Перейдите в браузер на: $API_URL/docs"
echo
