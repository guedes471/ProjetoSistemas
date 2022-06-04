import socket
from time import sleep, time

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server.sendto("reator".encode(), ('localhost', 12000))


def enviar(msg):
    server.sendto(msg.encode(), ('localhost', 12000))

pronto = False

while not pronto:
    msgBytes =server.recv(2048)
    if msgBytes.decode() == "pronto":
        pronto = True

inicio = time()
fim =  time()

while fim - inicio <= 3600:
    sleep(1)
    enviar("processar")
    enviar("vazao")
