from random import random
import socket
from time import sleep, time
from codigos import codigo


server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server.sendto("oleo".encode(), ('localhost', 12000))
qtd = 0

def mensagem(qtd):
    msg = str(codigo("OLEO")) + " " + str(qtd)
    server.sendto(msg.encode(), ("localhost",12000))
pronto = False

while not pronto:
    msgBytes =server.recv(2048)
    if msgBytes.decode() == "pronto":
        pronto = True


tempo = 0

inicio = time()
fim =  time()

while fim - inicio <= 3600:
    if tempo == 0:
        tempo = int(1 + random() * 9)
        qtd += 1 + random()

    if qtd == 0:
        tempo -= 1
        sleep(1)
        continue
    if(qtd > 0.75):
        mensagem(0.75)
        msgBytes =server.recv(2048)
        retirado = float(msgBytes.decode())
        qtd -= retirado
    else:
        mensagem(qtd)
        msgBytes =server.recv(2048)
        retirado = float(msgBytes.decode())
        qtd -= retirado
        
    tempo -= 1




    msgMonitor = "------\nQuantidade de oleo no tanque de oleo: " + str(qtd) + "\n------\n"
    print(msgMonitor)
    
    sleep(1)
    
    
    
    
    
    

    







