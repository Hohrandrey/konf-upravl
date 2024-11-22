# mermaid_generator.py
def generate_mermaid_graph(package_name, dependencies):
    """
    Генерирует строку в формате Mermaid для визуализации зависимостей.
    """
    graph = f"graph LR\n"
    graph += f"  {package_name} --> " + " --> ".join(dependencies) + "\n"
    return graph
