"""
* Внутренние типы данных и константы в рамках проекта
* *************************
* В данном файле хранятся внутренние типы данных и константы,
* которые созданы для нужд работы проекта.
*
* @author Ефремов А. В., 01.08.2025
"""

from collections import namedtuple
from enum import Enum

ConnSocket = namedtuple("ConnSocket", ["host", "port"])

class Constant(Enum):
    GLOBAL_CODEPAGE = "cp1251" # кодировка Windows-1251 в текстовых файлах
    SETTINGS_FILE = "settings.ini"  # путь к файлу конфигурации
