import re
import xml.etree.ElementTree as ET

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
        elif '(' in value:  # Это выражение для вычисления
            value = self.evaluate_expression(value)
        self.variables[name] = value

    def parse_array(self, array_str):
        values = array_str[1:-1].split()
        return [int(v) for v in values]

    def evaluate_expression(self, expr):
        # Пример постфиксной формы
        tokens = expr[1:].split()
        print(tokens)
        name = tokens[0]
        print("name"+name)
        operation = tokens[1]
        print("operation"+operation)
        operand = tokens[2]
        value = self.variables[name]
        if operation == "+":
            return value + operand
        elif operation == "-":
            return value - operand
        elif operation == "pow":
            return pow(value, operand)
        elif operation == "len":
            return len(self.variables[name])
        return 0

    def parse(self, input_text):
        # Пример регулярных выражений для поиска конструкций
        define_regex = r"\(define (\w+) (.+?)\)"
        operation_regex = r"!(\(\w+ .+\))"

        defines = re.finditer(define_regex, input_text)
        for match in defines:
            self.parse_define(match)

    def to_xml(self):
        root = ET.Element("configuration")
        for name, value in self.variables.items():
            if isinstance(value, list):
                value = f"[{', '.join(map(str, value))}]"
            ET.SubElement(root, "define", name=name, value=str(value))
        return ET.tostring(root, encoding="unicode")

# Основная логика программы
def main():
    with open('input.txt', 'r') as infile:
        input_text = infile.read()

    parser = ConfigParser()
    parser.parse(input_text)

    output_xml = parser.to_xml()

    with open('output.txt', 'w') as outfile:
        outfile.write(output_xml)

if __name__ == "__main__":
    main()
