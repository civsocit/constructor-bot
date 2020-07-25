# constructor-bot
Telegram бот конструктор плакатов для Гражданского Общества

Установка зависимостей и запуск:
```
poetry install --no-root
pre-commit install
poetry run bot
```

Файл .env должен лежать в корне проекта:
```
TOKEN="Ваш токен Telegram"
```
Либо переменная окружения TOKEN должна быть задана

Перед новым коммитом запустите `make pre-commit`