import sys
import os


def resource_path(relative_path: str) -> str:
    """
    Получает абсолютный путь к ресурсу, работает как для разработки,
    так и для сборки через PyInstaller.

    Args:
        relative_path: Относительный путь к файлу ресурса.

    Returns:
        Абсолютный путь к файлу ресурса.
    """
    try:
        # PyInstaller создает временную папку и сохраняет путь в "_MEIPASS"
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
