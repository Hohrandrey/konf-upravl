import re
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Класс для работы с конфигурацией
class ConfigParser:
    def __init__(self):
        self.variables = {}

    def parse_define(self, match):
        name = match.group(1)
        value = match.group(2)
        if value.startswith('[') and value.endswith(']'):
            value = self.parse_array(value)
        elif value.isdigit():
            value = int(value)
        elif value.startswith('!'):  # Это выражение для вычисления
            value = self.evaluate_expression(value)
        else:
            # Некорректное значение, если оно не массив, не число и не выражение
            raise ValueError(f"Некорректное значение для переменной {name}: {value}")

        self.variables[name] = value

    def parse_array(self, array_str):
        values = array_str[1:-1].split()
        try:
            return [int(v) for v in values]
        except ValueError:
            raise ValueError(f"Некорректные элементы массива: {array_str}")

    def evaluate_expression(self, expr):
        # Убираем "!" и "(", ")" вокруг выражения, чтобы работать с чистой постфиксной формой
        if expr[0] == "!":
            expr = expr[2:].strip()  # Убираем "!" и оставляем выражение
        tokens = expr.split()


        # Первый элемент - это имя переменной
        name = tokens[0]
        if name not in self.variables:
            raise ValueError(f"Переменная {name} не определена в момент вычисления выражения: {expr}")

        value = self.variables[name]

        # Далее идут операции, будем выполнять их поочередно
        for i in range(1, len(tokens), 2):
            operation = tokens[i]
            if len(tokens) == 3:
                try:
                    operand = int((tokens[i + 1])[:-1])
                except ValueError:
                    raise ValueError(f"Неправильный ввод команды")

            if operation == "+":
                value += operand
                self.variables["plus"] = value  # Сохраняем результат в переменную "plus"
            elif operation == "-":
                value -= operand
                self.variables["minus"] = value  # Сохраняем результат в переменную "minus"
            elif operation == "pow":
                value = pow(value, operand)
                self.variables["pow"] = value  # Сохраняем результат в переменную "pow"
            elif operation == "len)":
                # Операция len применима только к массивам
                if isinstance(self.variables[name], list):
                    value = len(self.variables[name])
                    self.variables["len_result"] = value  # Сохраняем результат в переменную "len_result"
                else:
                    raise ValueError(f"len() можно применить только к массиву, а не к {type(self.variables[name])}")
            else:
                raise ValueError(f"Неизвестная операция: {operation}")

        return value

    def parse(self, input_text):
        # Пример регулярных выражений для поиска конструкций
        define_regex = r"\(define (\w+) (.+?)\)"
        operation_regex = r"!(\(\w+ .+\))"  # Регулярное выражение для поиска операций

        defines = re.finditer(define_regex, input_text)
        for match in defines:
            self.parse_define(match)

        # Обрабатываем постфиксные выражения
        operations = re.finditer(operation_regex, input_text)
        for match in operations:
            operation_expr = match.group(0)
            # Результат операции записывается только в нужные переменные
            self.evaluate_expression(operation_expr)

    def to_xml(self):
        # Создаем пустую строку для хранения результирующего XML
        result = ""

        for name, value in self.variables.items():
            # Преобразуем значение в строку, если это массив, то в строку вида [1, 2, 3]
            if isinstance(value, list):
                value = f"[{', '.join(map(str, value))}]"
            # Записываем только переменные, не содержащие "!".
            # Избегаем записей вида !(x pow 3)
            if not name.startswith("!("):
                result += f"<{name}>{value}</{name}>\n"

        # Возвращаем результат
        return result


# Основная логика программы
def main():
    try:
        with open('input1.txt', 'r') as infile:
            input_text = infile.read()

        # Проверка на пустоту входных данных
        if not input_text.strip():
            raise ValueError("Входной файл пуст.")

        parser = ConfigParser()
        parser.parse(input_text)

        output_xml = parser.to_xml()

        with open('output1.txt', 'w') as outfile:
            outfile.write(output_xml)

        print("XML файл успешно записан.")

    except ValueError as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
