# PostgreSQL Verification Results

Дата проверки: 2026-06-11

## Подключение к БД

```
Host: localhost
Port: 5432
Database: octagon_db
User: octagon
```

## Таблица Categories

```sql
SELECT * FROM categories ORDER BY id;
```

Результат:
```
 id |       title        
----+--------------------
  1 | Fiction
  2 | Non-fiction
  3 | Тестовая категория
  4 | Science Fiction
(4 rows)
```

**Статистика:**
- Всего категорий: 4
- Все категории получены через API и созданы/обновлены корректно
- Каскадное удаление работает (при удалении категории удаляются связанные книги)

## Таблица Books

```sql
SELECT id, title, price, category_id FROM books ORDER BY id;
```

Результат:
```
 id |                    title                    | price | category_id 
----+---------------------------------------------+-------+-------------
  1 | The Strange Case of Dr. Jekyll and Mr. Hyde |  8.99 |           1
  2 | 1984                                        | 11.50 |           1
  3 | Sapiens: A Brief History of Humankind       | 14.99 |           2
  4 | Atomic Habits                               | 12.80 |           2
  5 | Тестовая книга                              | 99.99 |           3
(5 rows)
```

**Статистика:**
- Всего книг: 5
- Книги в категории 1 (Fiction): 2
- Книги в категории 2 (Non-fiction): 2
- Книги в категории 3 (Тестовая категория): 1
- Все цены корректны
- Все foreign keys указывают на существующие категории

## Проверка целостности данных

```sql
-- Проверить что все category_id указывают на существующие категории
SELECT COUNT(*) FROM books 
WHERE category_id NOT IN (SELECT id FROM categories);
```

Результат: 0 (все данные целостны)

## Синхронизация с API

✅ **Категории:**
- Все категории из БД видны в `GET /categories/`
- Создание категории через API создает запись в БД
- Обновление категории через API обновляет данные в БД
- Удаление категории через API удаляет запись из БД

✅ **Книги:**
- Все книги из БД видны в `GET /books/`
- Создание книги через API создает запись в БД
- Обновление книги через API обновляет данные в БД
- Удаление книги через API удаляет запись из БД
- Фильтрация по category_id работает корректно

## Constraints и Relations

```sql
-- Проверить foreign keys
SELECT * FROM information_schema.table_constraints 
WHERE table_name = 'books' AND constraint_type = 'FOREIGN KEY';
```

**Результат:** Foreign key на category_id → categories.id работает корректно

## Conclusion

✅ База данных полностью синхронизирована с API
✅ Все CRUD операции работают корректно
✅ Целостность данных проверена
✅ Foreign keys работают правильно
✅ Каскадное удаление настроено
