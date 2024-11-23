# dependency_visualizer.py
import subprocess
import sys
import os
from mermaid_generator import generate_mermaid_graph
from dependency_extractor import extract_dependencies


def visualize_dependencies(package_name, visualizer_path):
    # Извлекаем зависимости пакета
    dependencies = extract_dependencies(package_name)

    # Генерируем Mermaid-граф зависимостей
    mermaid_graph = generate_mermaid_graph(package_name, dependencies)

    # Выводим Mermaid-граф на экран
    print("Mermaid graph:\n", mermaid_graph)

    # Сохраняем граф в файл
    graph_file = 'dependencies.mmd'
    with open(graph_file, 'w') as file:
        file.write(mermaid_graph)

    # Визуализируем граф через внешнюю программу
    subprocess.run([visualizer_path, graph_file])


if __name__ == "__main__":
    # Чтение аргументов командной строки
    if len(sys.argv) != 3:
        print("Usage: python dependency_visualizer.py <path_to_visualizer> <package_name>")
        sys.exit(1)

    visualizer_path = sys.argv[1]
    package_name = sys.argv[2]

    visualize_dependencies(package_name, visualizer_path)
