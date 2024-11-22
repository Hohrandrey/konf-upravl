# visualizer_cli.py
import argparse
from dependency_visualizer import visualize_dependencies


def main():
    # Настроим аргументы командной строки
    parser = argparse.ArgumentParser(description="Visualize Python package dependencies using Mermaid.")
    parser.add_argument("visualizer_path", help="Path to the graph visualizer program (e.g., Mermaid Live Editor).")
    parser.add_argument("package_name", help="Name of the Python package to visualize dependencies for.")

    args = parser.parse_args()

    # Проверим, что имя пакета не пустое
    if not args.package_name:
        print("Error: Package name cannot be empty.")
        return

    print(f"Visualizing dependencies for package: {args.package_name}")

    # Запускаем визуализацию зависимостей
    try:
        visualize_dependencies(args.package_name, args.visualizer_path)
    except Exception as e:
        print(f"An error occurred while visualizing dependencies: {e}")


if __name__ == "__main__":
    main()