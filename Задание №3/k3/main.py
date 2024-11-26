import re
import xml.etree.ElementTree as ET
from xml.dom import minidom  # Для красивого форматирования XML

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
        self.variables[name] = value

    def parse_array(self, array_str):
        values = array_str[1:-1].split()
        return [int(v) for v in values]

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
            if len(tokens) > 2:
                operand = int((tokens[i + 1])[:-1])

            if operation == "+":
                value += operand
            elif operation == "-":
                value -= operand
            elif operation == "pow":
                value = pow(value, operand)
            elif operation == "len)":
                # Операция len применима только к массивам
                if isinstance(self.variables[name], list):
                    value = len(self.variables[name])
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
            result = self.evaluate_expression(operation_expr)
            # Записываем результат в переменную с именем, соответствующим операции
            self.variables[operation_expr] = result  # Используем само выражение как имя переменной

    def to_xml(self):
        root = ET.Element("configuration")
        for name, value in self.variables.items():
            if isinstance(value, list):
                value = f"[{', '.join(map(str, value))}]"
            ET.SubElement(root, "define", name=name, value=str(value))

        # Преобразуем в строку и форматируем с использованием minidom
        rough_xml = ET.tostring(root, encoding="unicode")
        parsed_xml = minidom.parseString(rough_xml)

        # Используем topyrettyxml без xml_declaration и удаляем строку с декларацией XML
        pretty_xml = parsed_xml.toprettyxml(indent="  ")

        # Удаляем строку с декларацией XML, если она есть
        lines = pretty_xml.splitlines()
        if lines[0].startswith("<?xml"):
            lines = lines[1:]
        return "\n".join(lines)


# Основная логика программы
def main():
    with open('input1.txt', 'r') as infile:
        input_text = infile.read()

    parser = ConfigParser()
    parser.parse(input_text)

    output_xml = parser.to_xml()

    with open('output1.txt', 'w') as outfile:
        outfile.write(output_xml)


if __name__ == "__main__":
    main()
