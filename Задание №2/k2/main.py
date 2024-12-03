import argparse
import subprocess
import pkg_resources
from PIL import Image, ImageDraw, ImageFont


# Функция для получения зависимостей пакета
def get_dependencies(package_name):
    """Получить транзитивные зависимости пакета через pip."""
    result = subprocess.run(['pip', 'show', package_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise ValueError(f"Не удалось получить информацию о пакете {package_name}")

    installed = result.stdout.decode('utf-8')
    dependencies = []

    for line in installed.splitlines():
        if line.startswith("Requires"):
            dependencies = line.split(":")[1].strip().split(", ")
            break

    return dependencies


# Генерация графа в формате Mermaid
def generate_mermaid_graph(package_name):
    """Генерируем строку Mermaid для графа зависимостей."""
    dependencies = get_dependencies(package_name)

    graph = f"graph TD\n  {package_name} -->|depends on| {', '.join(dependencies)}"
    return graph


# Функция для визуализации Mermaid в изображение
def visualize_mermaid_graph(mermaid_code, output_path):
    """Визуализирует Mermaid граф с использованием Pillow."""
    img = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(img)

    # Для простоты, выводим Mermaid код как текст на картинке
    font = ImageFont.load_default()
    draw.text((10, 10), mermaid_code, font=font, fill="black")

    img.save(output_path)
    img.show()


# Основная логика работы инструмента командной строки
def main():
    parser = argparse.ArgumentParser(description="Визуализатор зависимостей Python пакетов")
    parser.add_argument("package", help="Имя пакета для анализа зависимостей")
    parser.add_argument("output", help="Путь для сохранения изображения графа")

    args = parser.parse_args()

    # Генерация графа зависимостей
    mermaid_code = generate_mermaid_graph(args.package)

    # Визуализация в изображение
    visualize_mermaid_graph(mermaid_code, args.output)


if __name__ == "__main__":
    main()
