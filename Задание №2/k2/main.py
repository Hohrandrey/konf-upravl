import argparse
import subprocess
import sys


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


# Генерация графа в формате Mermaid
def generate_mermaid_graph(package_name, output_file_path):
    """Генерируем граф зависимостей в формате Mermaid."""
    dependencies, dependency_hierarchy = get_dependencies(package_name)

    # Открываем файл для записи
    with open(output_file_path, 'w') as f:
        f.write("graph TD\n")  # Указываем тип графа (Directed Graph)

        # Функция для добавления зависимостей в Mermaid-формате
        def add_dependencies(parent, dependencies):
            for dependency in dependencies:
                if dependency.strip():  # Проверяем, что зависимость не пустая
                    f.write(
                        f"    {parent} --> {dependency}\n")  # Добавляем ребро между родительским пакетом и зависимостью

                    # Рекурсивно добавляем подзависимости
                    if dependency in dependency_hierarchy:
                        add_dependencies(dependency, dependency_hierarchy[dependency])

        # Добавляем основной пакет
        f.write(f"    {package_name}\n")

        # Запуск рекурсивной функции для добавления зависимостей
        add_dependencies(package_name, dependencies)


# Основная логика работы инструмента командной строки
def main():
    parser = argparse.ArgumentParser(description="Визуализатор зависимостей Python пакетов в формате Mermaid")
    parser.add_argument("package", help="Имя пакета для анализа зависимостей")
    parser.add_argument("mermaid_cli_path", help="Путь к программе для визуализации графов (Mermaid CLI)")

    args = parser.parse_args()

    # Генерация графа зависимостей в формате Mermaid
    try:
        mermaid_file_path = "graph.mmd"  # Имя файла, куда будет сохранен граф Mermaid
        output_image_path = "graph.png"  # Всегда сохраняем граф как PNG

        # Генерация графа
        generate_mermaid_graph(args.package, mermaid_file_path)
        print(f"Граф зависимостей успешно записан в файл: {mermaid_file_path}")

        # Используем Mermaid CLI для генерации изображения
        result = subprocess.run(
            [args.mermaid_cli_path, "-i", mermaid_file_path, "-o", output_image_path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=60  # Добавили timeout
        )

        if result.returncode != 0:
            raise ValueError(f"Ошибка при генерации изображения: {result.stderr}")

        print(f"Изображение графа успешно сохранено в файл: {output_image_path}")
        sys.exit(0)  # Явное завершение программы с успешным кодом

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        sys.exit(1)  # Если произошла ошибка, программа завершится с кодом ошибки


if __name__ == "__main__":
    main()