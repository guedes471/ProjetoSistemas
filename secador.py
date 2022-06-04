import socket
from time import sleep, time

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server.sendto("secador".encode(), ('localhost', 12000))

pronto = False

while not pronto:
    msgBytes =server.recv(2048)
    if msgBytes.decode() == "pronto":
        pronto = True

qtd = 0.0

def receber():
    global qtd
    server.sendto("receber 1".encode(), ('localhost', 12000))
    msgBytes =server.recv(2048)
    recebido = float(msgBytes.decode())
    if recebido > 0:
        perda = recebido * 0.005
        server.sendto(("perda " + str(perda)).encode(), ('localhost', 12000))
        qtd += recebido * 0.995
    sleep(1)
        

def enviar():
    global qtd
    if qtd > 0:
        if qtd <= 0.2:
            server.sendto(("saida " + str(qtd)).encode(), ('localhost', 12000))
            qtd = 0
        else:
            server.sendto("saida 0.2".encode(), ('localhost', 12000))
            qtd -= 0.2
    
    msgMonitor = "------\nQuantidade no secador: " + str(qtd) + "\n------"
    print(msgMonitor)
        
inicio = time()
fim =  time()

while fim - inicio <= 3600:
    enviar()
    receber()





