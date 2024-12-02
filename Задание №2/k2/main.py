import subprocess
import sys
import os
import json
import argparse
import unittest


def get_dependencies(package_name):
    """
    Получить зависимости для указанного пакета, включая транзитивные.
    """
    dependencies = {}

    # Получаем список зависимостей с помощью pipdeptree
    result = subprocess.run(['pipdeptree', '--json'], stdout=subprocess.PIPE, text=True)

    if result.returncode != 0:
        print(f"Ошибка при получении зависимостей для пакета {package_name}")
        sys.exit(1)

    packages = json.loads(result.stdout)

    # Строим словарь зависимостей
    for pkg in packages:
        if pkg['package']['key'] == package_name:
            dependencies[pkg['package']['key']] = [dep['package']['key'] for dep in pkg.get('dependencies', [])]

    return dependencies


def generate_mermaid_graph(dependencies):
    """
    Генерирует строку для визуализации графа зависимостей в формате Mermaid.
    """
    graph = "graph TD\n"

    # Проходим по зависимостям и строим граф
    for package, deps in dependencies.items():
        for dep in deps:
            graph += f"    {package} --> {dep}\n"

    return graph


def visualize_graph(graph, visualizer_path):
    """
    Визуализирует граф, используя внешний инструмент для работы с Mermaid.
    """
    # Сохраняем граф в файл
    with open('graph.mmd', 'w') as f:
        f.write(graph)

    # Запускаем внешний инструмент для визуализации
    subprocess.run([visualizer_path, 'graph.mmd'], check=True)


def main():
    parser = argparse.ArgumentParser(description='Визуализатор зависимостей Python-пакетов')
    parser.add_argument('visualizer_path', help='Путь к программе для визуализации графов (например, mermaid-cli)')
    parser.add_argument('package_name', help='Имя анализируемого пакета')
    args = parser.parse_args()

    # Получаем зависимости
    dependencies = get_dependencies(args.package_name)

    # Генерируем граф в формате Mermaid
    graph = generate_mermaid_graph(dependencies)

    # Визуализируем граф
    visualize_graph(graph, args.visualizer_path)


if __name__ == '__main__':
    main()
