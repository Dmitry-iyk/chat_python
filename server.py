# Импорт нужных модулей (Дима Зянкин)
import time
from socket import gethostbyname, gethostname, socket, AF_INET, SOCK_DGRAM


# Объявление сокетов и протокола UDP для работы сервера (Карина Трофимова)
# Переменные принимающие в себе IP и свободный порт
host = gethostbyname(gethostname())
port = 10033
# Список клиентов
clients = []
# Использование семества сетевых сокетов и протокол UDP
s = socket(AF_INET, SOCK_DGRAM)
# Создание хоста и порта
s.bind((host, port))

quit = False
print("[ Server Started ]")


# Работа самого сервера (Коля Николаев)
while not quit:
    # Приём и отправка пакетов клиентам
    try:
        # Data - сообщение, addr - личный адрес пользователя
        data, addr = s.recvfrom(1024)
        # Добавление клиентов
        if addr not in clients:
            clients.append(addr)
        # Текущее время добавления клиента
        itsatime = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())

        print("[" + addr[0] + "]=[" + str(addr[1]) + "]=[" + itsatime + "]/", end="")
        # Перевод кодировки в байты
        print(data.decode("utf-8"))
        # Отправка сообщения и имени клиента другим участникам чата, но не себе
        for client in clients:
            if addr != client:
                s.sendto(data, client)
    # Если сервер выводит ошибку останавливаем сервер (UDP и IP не используются)
    except:
        print("\n[ Server Stopped ]")
        quit = True


s.close()
