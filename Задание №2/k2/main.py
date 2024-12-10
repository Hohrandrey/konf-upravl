import argparse
import subprocess
from graphviz import Digraph

# Функция для получения зависимостей пакета (рекурсивно)
def get_dependencies(package_name, visited=None):
    """Получить транзитивные зависимости пакета через pip."""
    if visited is None:
        visited = set()

    # Проверка, чтобы избежать бесконечной рекурсии
    if package_name in visited:
        return [], {}

    visited.add(package_name)

    # Получаем зависимости через pip show
    result = subprocess.run(['pip', 'show', package_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise ValueError(f"Не удалось получить информацию о пакете {package_name}")

    installed = result.stdout
    dependencies = []
    dependency_hierarchy = {}

    for line in installed.splitlines():
        if line.startswith("Requires"):
            # Разделяем зависимости и убираем пробелы
            dependencies = [dep.strip() for dep in line.split(":")[1].strip().split(", ") if dep.strip()]
            break

    # Получаем транзитивные зависимости для каждого элемента, но только на уровне первого уровня
    for dependency in dependencies:
        if dependency:  # Проверяем, что зависимость не пустая
            sub_dependencies, sub_hierarchy = get_dependencies(dependency, visited)
            dependency_hierarchy[dependency] = sub_hierarchy

    # Убираем дубликаты и возвращаем иерархию зависимостей
    return list(set(dependencies)), dependency_hierarchy

# Генерация графа с учетом иерархии зависимостей
def generate_graphviz_graph(package_name, output_image_path):
    """Генерируем граф зависимостей с использованием graphviz с учетом иерархии зависимостей."""
    dependencies, dependency_hierarchy = get_dependencies(package_name)
    dot = Digraph(format='png')
    dot.node(package_name, package_name)  # Добавляем основной пакет

    # Рекурсивная функция для добавления узлов и ребер с учетом иерархии
    def add_dependencies(parent, dependencies):
        for dependency in dependencies:
            if dependency.strip():  # Проверяем, что зависимость не пустая
                dot.node(dependency, dependency)  # Добавляем зависимость
                dot.edge(parent, dependency)  # Соединяем родительский узел с зависимостью

                # Добавляем подзависимости только на уровне одного уровня вложенности
                if dependency in dependency_hierarchy:
                    add_dependencies(dependency, dependency_hierarchy[dependency])

    # Запуск рекурсивной функции для добавления зависимостей первого уровня
    add_dependencies(package_name, dependencies)

    dot.render(output_image_path, cleanup=True)  # Сохраняем изображение

# Основная логика работы инструмента командной строки
def main():
    parser = argparse.ArgumentParser(description="Визуализатор зависимостей Python пакетов")
    parser.add_argument("package", help="Имя пакета для анализа зависимостей")
    parser.add_argument("output", help="Путь для сохранения файла изображения графа")

    args = parser.parse_args()

    # Генерация графа зависимостей
    try:
        generate_graphviz_graph(args.package, args.output)
        print(f"Граф зависимостей успешно записан в изображение: {args.output}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
