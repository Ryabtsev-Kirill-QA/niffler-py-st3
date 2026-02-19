- Понадобится Docker Desktop - для запуска контейнеров
- Все команды выполняются в Git Bash
- Также понадобится скачать Java 21 для запуска приложения
- env.example надо скопировать в .env и вписать туда креды

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

Аргументы для формирования отчета Allure
```
--alluredir=allure-results --clean-alluredir
```
для отображения отчета allure serve (Allure должен быть в Path)