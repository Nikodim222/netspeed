"""
* netspeed
* *************************
* Клиентская часть программы для измерения скорости сети.
*
* @author Ефремов А. В., 01.08.2025
"""

from socket import socket, AF_INET, SOCK_STREAM
import time

from models import ConnSocket
from configuration import Configuration

MB: int = 2 # мегабайты

connSocket: ConnSocket = None

def measure_speed(host: str, port: int, data_size: int) -> float:
    global MB
    speed: float = 0
    with socket(AF_INET, SOCK_STREAM) as s:
        try:
            start_time = time.time()
            s.connect((host, port))
            data: str = b'A' * data_size  # Создаем данные для отправки
            s.sendall(data)
            received_data: str = b''
            while len(received_data) < data_size:
                chunk = s.recv(4096)
                if not chunk:
                    break
                received_data += chunk
            end_time = time.time()
            duration = end_time - start_time
            speed = (data_size / duration) / pow(1024, MB)  # MB/s
        except (ConnectionRefusedError, ConnectionResetError):
            speed = 0
    return speed

def main() -> None:
    global MB
    global connSocket
    is_running: bool = True # признак работы программы
    print("netspeed (клиент)")
    print("*************************")
    print("Для выхода из программы введите пустую строку или нажмите Ctrl+C.")
    objConfiguration: Configuration = Configuration()
    connSocket = objConfiguration.get_config()
    is_running = objConfiguration.get_running()
    objConfiguration.print_config()
    if is_running == True:
        try:
            HOST: str = connSocket.host         # IP-адрес сервера
            PORT: int = connSocket.port         # Порт сервера
            DATA_SIZE: int = pow(1024, MB) * 10 # 10 MB
            speed: float = measure_speed(HOST, PORT, DATA_SIZE)
            print(f"Скорость: {speed:.2f} Мбайт/с")
        except KeyboardInterrupt: # перехват Ctrl+C
            print()
            is_running = False
    print("Работа программы завершена.")

# Точка запуска программы
if __name__ == "__main__":
    main()
