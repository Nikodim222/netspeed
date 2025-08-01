import configparser

from models import ConnSocket, Constant

class Configuration:
    """
    * Класс для работы с конфигурацией программы
    """

    is_running: bool = True # признак работы программы (по умолчанию работает программа)
    connSocket: ConnSocket = None

    def __init__(self):
        self.connSocket = self.run_config()

    def run_config(self) -> ConnSocket:
        """
        * Получение конфигурации
        *
        * return ConnSocket
        """
        GLOBAL_SECTION: str = "global"
        HOST: str = "host"
        PORT: str = "port"
        config = configparser.ConfigParser()
        try:
            with open(Constant.SETTINGS_FILE.value, 'r', encoding=Constant.GLOBAL_CODEPAGE.value) as f:
                config.read_file(f)
                if GLOBAL_SECTION in config and HOST in config[GLOBAL_SECTION]:
                    v_host: str = config[GLOBAL_SECTION][HOST].strip()
                if GLOBAL_SECTION in config and PORT in config[GLOBAL_SECTION]:
                    v_port: int = config.getint(GLOBAL_SECTION, PORT)
                if not (1 <= v_port <= 65534):
                    raise ValueError("Значение порта вне допустимого диапазона (1 - 65534)")
                return ConnSocket(host=v_host, port=v_port)
        except FileNotFoundError:
            print(f"Ошибка: Файл настроек не найден: {Constant.SETTINGS_FILE.value}")
            self.is_running = False
            return ConnSocket(host=None, port=None)
        except ValueError:
            print("Значение параметра не соответствует типу данных в конфигурационном файле.")
            self.is_running = False
            return ConnSocket(host=None, port=None)
        except Exception as e:
            print(f"Ошибка при чтении файла настроек: {e}")
            self.is_running = False
            return ConnSocket(host=None, port=None)

    def get_config(self) -> ConnSocket:
        """
        * Функцию возвращает текущую конфигурацию
        *
        * @return ConnSocket
        """
        return self.connSocket

    def get_running(self) -> bool:
        """
        * Функция возвращает признак работы программы
        * Если произошла какая-то ошибка, то признак выставляется
        * в логическое значение "ложь".
        *
        * @return bool
        """
        return self.is_running

    def print_config(self) -> None:
        """
        * Вывод на экран конфигурации программы
        """
        if self.get_running():
            connSocket: ConnSocket = self.get_config()
            print(f"Хост: {connSocket.host}")
            print(f"Порт: {connSocket.port}")
        else:
            print("При обработке конфигурации программы произошла ошибка.")
