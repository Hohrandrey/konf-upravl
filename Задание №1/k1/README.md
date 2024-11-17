# О проекте

Приложение, эмулирующее работу в командной строке Unix-подобной ОС.

# 1. Клонирование репозитория

Клонируйте репозиторий с исходным кодом и тестами:

```bash
git clone <URL репозитория>
cd <директория проекта>
```

# 2. Виртуальное окружение

```shell
python -m venv venv
venv/Scripts/activate
```

# 3. Установка зависимостей

```shell
pip install -r requirements.txt
```

# 4. Запуск программы

Запуск в режиме **GUI**:

```shell
py main.py "path.xml"
```

Запуск в режиме **CLI**:

```shell
py main.py "path.xml" -cli
```

# 5. Тестирование

Для запуска тестирования необходимо запустить следующий скрипт:

```shell
pytest -v
```

Для генерации отчета о покрытии тестами необходимо выполнить команду:

```shell
coverage run --branch -m pytest test_builder.py
```

Просмотр результатов покрытия:

```shell
coverage report
```

# Тесты

Для всех методов были написаны тесты, в результате удалось добиться покрытия в 79%.

### Прохождение тестов:

![pycharm64_oWhtEJ9Byy](https://github.com/user-attachments/assets/ee089558-c29e-406a-af16-002c26d60f7e)


### Процент покрытия:

![pycharm64_RTGIO3VjVe](https://github.com/user-attachments/assets/740961ef-bf06-4cf2-aff7-bd9757cca26c)
