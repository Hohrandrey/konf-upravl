import argparse
import subprocess
import os
import sys

# Функция для получения зависимостей пакета (рекурсивно)
def get_dependencies(package_name, visited=None):
    """Получить транзитивные зависимости пакета через pip."""
    if visited is None:
        visited = set()

    # Проверка, чтобы избежать бесконечной рекурсии
    if package_name in visited:
        return []

    visited.add(package_name)

    # Получаем зависимости через pip show
    result = subprocess.run(['pip', 'show', package_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise ValueError(f"Не удалось получить информацию о пакете {package_name}")

    installed = result.stdout
    dependencies = []

    for line in installed.splitlines():
        if line.startswith("Requires"):
            dependencies = line.split(":")[1].strip().split(", ")
            break

    # Получаем транзитивные зависимости для каждого элемента
    all_dependencies = []
    for dependency in dependencies:
        if dependency:  # Проверяем, что зависимость не пустая
            all_dependencies.append(dependency)
            all_dependencies.extend(get_dependencies(dependency, visited))

    return list(set(all_dependencies))  # Убираем дубликаты

# Генерация графа в формате Mermaid
def generate_mermaid_graph(package_name):
    """Генерируем строку Mermaid для графа зависимостей."""
    dependencies = get_dependencies(package_name)
    graph = "graph TD\n"
    for dependency in dependencies:
        graph += f"  {package_name} --> {dependency}\n"
    return graph

# Основная логика работы инструмента командной строки
def main():
    parser = argparse.ArgumentParser(description="Визуализатор зависимостей Python пакетов")
    parser.add_argument("package", help="Имя пакета для анализа зависимостей")
    parser.add_argument("output", help="Путь для сохранения файла Mermaid")

    args = parser.parse_args()

    # Генерация графа зависимостей
    try:
        mermaid_code = generate_mermaid_graph(args.package)
        with open(args.output, 'w') as f:
            f.write(mermaid_code)
        print(f"Граф зависимостей успешно записан в файл: {args.output}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()

