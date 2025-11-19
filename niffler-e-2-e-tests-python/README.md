Понадобится Docker Desktop - для запуска контейнеров

Установка и запуск (Windows)

В корне проекта (niffler-py-st3)
```
./docker-compose-dev.sh
```

Настройка скриптов (если требуется)
Исправление формата файлов для Windows
```
sed -i -e 's/\r$//' init-database.sh
chmod +x init-database.sh
```

Установка зависимостей Python
Переход в папку с E2E тестами
```
cd niffler-e-2-e-tests-python
```

Установка зависимостей через Poetry
```
poetry install
```

Установка браузеров для Playwright
```
poetry run playwright install
```

Запуск тестов
```
poetry run pytest
```

Запуск с медленным выполнением для отладки
```
poetry run pytest --headed --slowmo 1000
```

Скопируйте env.example в .env и настройте параметры подключения