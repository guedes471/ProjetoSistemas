import socket
from time import sleep, time

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server.sendto("decantador".encode(), ('localhost', 12000))

pronto = False

while not pronto:
    msgBytes =server.recv(2048)
    if msgBytes.decode() == "pronto":
        pronto = True

inicio = time()
fim =  time()

while fim - inicio <= 3600:

    server.sendto("lancar".encode(), ('localhost', 12000))
    server.sendto("printar".encode(), ('localhost', 12000))
    msgBytes =server.recv(2048)
    print(msgBytes.decode())
    sleep(1)
    