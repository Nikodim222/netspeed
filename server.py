"""
* netspeed
* *************************
* Серверная часть программы для измерения скорости сети.
*
* @author Ефремов А. В., 01.08.2025
"""

from socket import socket, AF_INET, SOCK_STREAM

from models import ConnSocket
from configuration import Configuration

connSocket: ConnSocket = None

def handle_client(conn, addr) -> None:
    print(f"Подключился клиент: {addr}")
    while True:
        data = conn.recv(1024)  # Получаем данные (размер буфера можно менять)
        if not data:
            break  # Клиент отключился
        conn.sendall(data)  # Отправляем данные обратно
    conn.close()
    print(f"Соединение с {addr} закрыто")

def main() -> None:
    global connSocket
    is_running: bool = True # признак работы программы
    print("netspeed (сервер)")
    print("*************************")
    print("Для выхода из программы введите пустую строку или нажмите Ctrl+C.")
    objConfiguration: Configuration = Configuration()
    connSocket = objConfiguration.get_config()
    is_running = objConfiguration.get_running()
    objConfiguration.print_config()
    HOST: str = "0.0.0.0"            # Слушаем на всех интерфейсах
    PORT: int = connSocket.port      # Порт для прослушивания
    if is_running == True:
        with socket(AF_INET, SOCK_STREAM) as s:
            try:
                s.bind((HOST, PORT))
                s.listen()
                print(f"Сервер слушает на {HOST}:{PORT}")
                while is_running == True:
                    try:
                        conn, addr = s.accept()
                        handle_client(conn, addr)
                    except (ConnectionRefusedError, ConnectionResetError):
                        print()
                        is_running = False
                    except KeyboardInterrupt: # перехват Ctrl+C
                        print()
                        is_running = False
            except (ConnectionRefusedError, ConnectionResetError):
                pass
    print("Работа программы завершена.")

# Точка запуска программы
if __name__ == "__main__":
    main()
