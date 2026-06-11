# Setup Instructions - Books API

Полная инструкция по настройке проекта с нуля.

## 🔧 Предварительные условия

1. **PostgreSQL 18.4+** установлен и запущен на localhost:5432
2. **Python 3.14+** установлен
3. **Git** установлен для клонирования репозитория

## 📥 Шаг 1: Клонировать репозиторий

```bash
git clone https://github.com/kaowow0p/DoingCrap.git
cd DoingCrap
```

## 🗄️ Шаг 2: Создать БД и пользователя в PostgreSQL

### Вариант A: Через sudo (рекомендуется для локальной разработки)

```bash
# Создать пользователя octagon и БД octagon_db
sudo -u postgres psql << EOF
DO \$$ BEGIN 
  IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'octagon') THEN 
    CREATE ROLE octagon LOGIN PASSWORD '12345'; 
  END IF; 
END \$$;

CREATE DATABASE octagon_db;
GRANT ALL PRIVILEGES ON DATABASE octagon_db TO octagon;
GRANT ALL PRIVILEGES ON SCHEMA public TO octagon;
EOF
```

### Вариант B: Через пароль postgres

```bash
psql -U postgres -h localhost << EOF
DO \$$ BEGIN 
  IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'octagon') THEN 
    CREATE ROLE octagon LOGIN PASSWORD '12345'; 
  END IF; 
END \$$;

CREATE DATABASE octagon_db;
GRANT ALL PRIVILEGES ON DATABASE octagon_db TO octagon;
GRANT ALL PRIVILEGES ON SCHEMA public TO octagon;
EOF
```

### Проверить создание

```bash
PGPASSWORD=12345 psql -U octagon -d octagon_db -h localhost -c "SELECT version();"
```

## 🐍 Шаг 3: Создать виртуальное окружение Python

```bash
python3 -m venv venv
. venv/bin/activate
```

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

## 📦 Шаг 4: Установить зависимости

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 🔐 Шаг 5: Создать файл .env

Создайте `.env` в корне проекта:

```bash
cat > .env << 'EOF'
DB_HOST=localhost
DB_PORT=5432
DB_NAME=octagon_db
DB_USER=octagon
DB_PASSWORD=12345
EOF
```

## 🗄️ Шаг 6: Инициализировать БД

```bash
python -m app.init_db
```

**Ожидаемый вывод:**
```
Seed data created.
Category 1: Fiction
  Book 1: The Strange Case of Dr. Jekyll and Mr. Hyde | price=8.99
  ...
```

## 🚀 Шаг 7: Запустить сервер

```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**Ожидаемый вывод:**
```
INFO:     Started server process
INFO:     Uvicorn running on http://127.0.0.1:8000
```

## ✅ Шаг 8: Проверить работу

### Способ 1: Swagger UI (рекомендуется)

Открыть в браузере:
```
http://127.0.0.1:8000/docs
```

Вы должны увидеть интерактивную документацию со всеми эндпоинтами.

### Способ 2: curl

```bash
# В другом терминале
curl http://127.0.0.1:8000/health
```

**Ожидаемый ответ:**
```json
{"status": "healthy", "service": "Books API"}
```

## 🧪 Шаг 9: Протестировать API

### Получить все книги
```bash
curl http://127.0.0.1:8000/books/ | jq .
```

### Получить все категории
```bash
curl http://127.0.0.1:8000/categories/ | jq .
```

### Создать новую категорию
```bash
curl -X POST http://127.0.0.1:8000/categories/ \
  -H "Content-Type: application/json" \
  -d '{"title": "My New Category"}'
```

**Ожидаемый ответ (код 201):**
```json
{"title": "My New Category", "id": 4}
```

## 🐛 Решение проблем

### Ошибка: `database "octagon_db" does not exist`

**Решение:**
```bash
sudo -u postgres createdb octagon_db
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE octagon_db TO octagon;"
```

### Ошибка: `permission denied for schema public`

**Решение:**
```bash
sudo -u postgres psql -d octagon_db -c "GRANT ALL PRIVILEGES ON SCHEMA public TO octagon;"
```

### Ошибка: `ModuleNotFoundError: No module named 'app'`

**Решение:**
- Убедитесь что находитесь в корне проекта
- Запускайте через `python -m uvicorn` (не `uvicorn`)

### Ошибка: `Port 8000 is already in use`

**Решение:**
```bash
# Использовать другой порт
python -m uvicorn app.main:app --port 8001

# Или убить процесс
lsof -ti:8000 | xargs kill -9
```

## 📝 Файловая структура после setup

```
DoingCrap/
├── .env                    # Переменные окружения (не коммитить!)
├── .env.example            # Пример .env для документации
├── .gitignore
├── README.md               # Основная документация
├── requirements.txt        # Python зависимости
├── venv/                   # Виртуальное окружение (не коммитить)
│
├── app/
│   ├── __init__.py
│   ├── main.py             # FastAPI приложение
│   ├── schemas.py          # Pydantic модели
│   ├── init_db.py          # Инициализация и seeding
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── categories.py   # Роуты категорий
│   │   └── books.py        # Роуты книг
│   │
│   └── db/
│       ├── __init__.py
│       ├── db.py           # Подключение к БД
│       ├── models.py       # SQLAlchemy модели
│       └── crud.py         # CRUD операции
│
└── examples/
    ├── README.md
    ├── TESTING.md
    ├── api_response_books.json
    ├── api_response_categories.json
    ├── postgresql_verify.txt
    └── *.png               # Скриншоты
```

## 🔒 Безопасность (для Production)

⚠️ **ВАЖНО:**

1. **Не коммитить .env** - используется для локальных переменных
2. **Изменить пароли** - в production использовать сильные пароли
3. **HTTPS** - использовать SSL/TLS сертификаты
4. **Аутентификация** - добавить JWT или API ключи
5. **Rate limiting** - ограничить количество запросов
6. **CORS** - настроить правильно для фронтенда

Пример для production:
```bash
# Использовать переменные окружения OS
export DB_PASSWORD=$(< /run/secrets/db_password)
export DB_USER=readonly_user

# Запустить с gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker \
  app.main:app --bind 0.0.0.0:8000 --ssl-keyfile=key.pem --ssl-certfile=cert.pem
```

## 📚 Дополнительные ресурсы

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## ✨ Готово!

API должен быть полностью функционален:
- [x] БД инициализирована
- [x] Сервер запущен
- [x] Swagger документация доступна
- [x] API готов к использованию

🎉 Поздравляем с успешной настройкой!
