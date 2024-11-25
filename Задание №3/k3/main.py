import re
import sys
import xml.etree.ElementTree as ET

# Регулярные выражения для синтаксического анализа
define_re = r"\(define\s+([a-zA-Z][_a-zA-Z0-9]*)\s+(.+?)\)"
expr_re = r"!\(([^)]+)\)"


def parse_define(match):
    name = match.group(1)
    value = match.group(2)
    return ET.Element("define", name=name, value=value)


def parse_expression(match):
    expr = match.group(1).split()
    variable = expr[0]
    operation = expr[1] if len(expr) > 1 else "unknown"

    # Создаем элемент для выражения
    expr_element = ET.Element("expression", value="unknown")
    variable_element = ET.SubElement(expr_element, "variable")
    variable_element.text = variable
    operation_element = ET.SubElement(expr_element, "operation")
    operation_element.text = operation
    return expr_element


def parse_input(input_text):
    config_element = ET.Element("config")

    # Ищем определения
    for match in re.finditer(define_re, input_text):
        config_element.append(parse_define(match))

    # Ищем выражения
    for match in re.finditer(expr_re, input_text):
        config_element.append(parse_expression(match))

    return config_element


def main():
    input_text = sys.stdin.read()
    config_element = parse_input(input_text)

    # Преобразуем в XML и выводим
    tree = ET.ElementTree(config_element)
    tree.write(sys.stdout, encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    main()
