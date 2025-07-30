import os
import sys


def resource_path(relative_path: str) -> str:
    """
    Получает абсолютный путь к ресурсу, работает как для разработки,
    так и для собранного в .exe приложения (PyInstaller).

    :param relative_path: Относительный путь к файлу из папки проекта.
    :return: Абсолютный путь к файлу.
    """
    try:
        # PyInstaller создает временную папку и сохраняет путь в "_MEIPASS"
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
