# Определение нужных модулей (Таланов Денис)
import threading
import time
from socket import gethostbyname, gethostname, socket, AF_INET, SOCK_DGRAM

# Реализации функции принимающей все данные и шифрование сообщений на сервере (Катя Лямзина)
# Ключ для шифровки данных
key = 8194

shutdown = False
join = False

# Принятие данных другого пользователя
def receving(name, sock):
    while not shutdown:
        try:
            while True:
                data, addr = sock.recvfrom(1024)
                # print(data.decode("utf-8"))

                # Begin
                decrypt = "";
                k = False
                for i in data.decode("utf-8"):
                    if i == ":":
                        k = True
                        decrypt += i
                    elif k == False or i == " ":
                        decrypt += i
                    else:
                        decrypt += chr(ord(i) ^ key)
                print(decrypt)
                # End

                time.sleep(0.2)
        except:
            pass

# Может принимать Ip разных пользователей, порт = 0, так как он не создаёт сеть, а только использует
host = gethostbyname(gethostname())
port = 0

server = (host,10033)
# Поднятие протоколов UDP и IP
s = socket(AF_INET, SOCK_DGRAM)
# Хост который использовали, а порт сервер распределит сам
s.bind((host, port))
# Неблокирующийрежим(справляет ошибки выхода из чата)
s.setblocking(0)

alias = input("Name: ")
# Многопоточность (отправление сообщений параллельно нескольких пользователей в одно время)
rT = threading.Thread(target=receving, args=("RecvThread", s))
rT.start()

# Пока клиент в сети может отправлять сообщения, если вышел уведомить сервер, реализвать деятельность клиентов (Егор)
while shutdown == False:
    if join == False:
        # Отправление сообщения на сервер о подключении клиента
        s.sendto(("[" + alias + "] => join chat ").encode("utf-8"), server)
        join = True
    else:
        try:
            message = input()

            # Begin кодировка сообщения на сервере
            crypt = ""
            for i in message:
                crypt += chr(ord(i) ^ key)
            message = crypt
            # End

            # Отправка сообщения клиента на сервер
            if message != "":
                s.sendto(("[" + alias + "] :: " + message).encode("utf-8"), server)

            time.sleep(0.2)
        # Выход из чата и уведомление на сервере о выходе клиента
        except:
            s.sendto(("[" + alias + "] <= left chat ").encode("utf-8"), server)
            shutdown = True

rT.join()
s.close()
