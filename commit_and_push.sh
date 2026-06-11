#!/bin/bash

cd /home/kaioshi/Documents/stupidThinks

# Активировать venv если еще не активирован
if [ -z "$VIRTUAL_ENV" ]; then
    . venv/bin/activate
fi

echo "=== Git Status ==="
git status --short

echo ""
echo "=== Adding files ==="
git add README.md examples/ app/api/ app/schemas.py app/main.py

echo ""
echo "=== Committing changes ==="
git commit -m "завершение: добавлены документация, примеры и тестирование API

- обновлен README с полной документацией
- добавлен TESTING.md с примерами curl запросов
- добавлены примеры ответов API (JSON)
- добавлены результаты проверки PostgreSQL
- обновлены роуты FastAPI с валидацией и правильными HTTP кодами
- все эндпоинты протестированы и работают"

echo ""
echo "=== Pushing to GitHub ==="
git push origin main

echo ""
echo "✓ Done! Changes pushed to GitHub"
echo ""
echo "Repository: https://github.com/kaowow0p/DoingCrap"
