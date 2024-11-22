# dependency_extractor.py
import subprocess
import sys


def extract_dependencies(package_name):
    if not package_name:
        raise ValueError("Package name cannot be empty.")

    try:
        # Используем pip для получения информации о пакете
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", package_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Если команда не выполнена успешно
        if result.returncode != 0:
            raise Exception(f"Package {package_name} not found.")

        # Извлекаем информацию о зависимостях
        dependencies = []
        for line in result.stdout.decode().splitlines():
            if line.startswith("Requires"):
                # Разбираем список зависимостей
                dependencies = line[len("Requires: "):].split(", ")
                break

        # Возвращаем список зависимостей
        return dependencies

    except Exception as e:
        print(f"Error while extracting dependencies for package {package_name}: {e}")
        raise