import pytest
from io import StringIO
from unittest.mock import patch
from main import ConfigParser  # Подключаем класс из файла main.py


# Тест на правильное определение переменных
def test_parse_define():
    input_text = "(define x 42)\n(define y [1 2 3])\n"

    parser = ConfigParser()
    parser.parse(input_text)

    assert parser.variables['x'] == 42
    assert parser.variables['y'] == [1, 2, 3]


# Тест на выполнение математических операций
def test_parse_operations():
    input_text = """
    (define x 10)
    (define y 20)
    !(x + 5)
    !(y - 5)
    """

    parser = ConfigParser()
    parser.parse(input_text)

    # Проверяем результат выполнения операций
    assert parser.variables['plus'] == 15
    assert parser.variables['minus'] == 15


# Тест на выполнение операций с массивами
def test_array_operations():
    input_text = """
    (define x [1 2 3 4])
    !(x len)
    """

    parser = ConfigParser()
    parser.parse(input_text)

    # Проверка длины массива
    assert parser.variables['len'] == 4


# Тест на некорректные операции (ошибка)
def test_invalid_operations():
    input_text = """
    (define x 10)
    !(x unknown_op 5)
    """

    parser = ConfigParser()

    # Проверка на выбрасывание ошибки при неизвестной операции
    with pytest.raises(ValueError, match="Неизвестная операция: unknown_op"):
        parser.parse(input_text)


# Тест на преобразование в XML
def test_to_xml():
    input_text = """
    (define x 10)
    (define y [1 2 3])
    !(x + 5)
    """

    parser = ConfigParser()
    parser.parse(input_text)

    # Ожидаемый XML-вывод
    expected_xml = """
<x>10</x>
<y>[1, 2, 3]</y>
<plus>15</plus>"""

    output_xml = parser.to_xml()

    # Сравниваем с ожидаемым результатом
    assert output_xml.strip() == expected_xml.strip()


# Тест на парсинг пустого входного текста
def test_empty_input():
    input_text = ""

    parser = ConfigParser()
    parser.parse(input_text)

    assert parser.variables == {}


# Тест на работу с входным файлом (используя patch для mock-объекта)
@patch("builtins.open", new_callable=lambda: StringIO("(define x 10)\n(define y 20)\n!(x + 5)"))
def test_main_function(mock_file):
    parser = ConfigParser()

    # Чтение из mock-файла
    input_text = mock_file.read()

    parser.parse(input_text)

    # Проверка переменных после парсинга
    assert parser.variables['x'] == 10
    assert parser.variables['y'] == 20
    assert parser.variables['plus'] == 15

    # Проверка на корректность XML
    output_xml = parser.to_xml()
    expected_xml = """
<x>10</x>
<y>20</y>
<plus>15</plus>"""

    assert output_xml.strip() == expected_xml.strip()
