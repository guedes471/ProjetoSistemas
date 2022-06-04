import socket
from time import sleep, time
from codigos import codigo

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def mensagem(qtd, produto):
    msg =str(codigo(produto) + " " + str(qtd))
    server.sendto(msg.encode(), ("localhost",12000))


server.sendto("naetoh".encode(), ('localhost', 12000))

pronto = False

while not pronto:
    msgBytes =server.recv(2048)
    if msgBytes.decode() == "pronto":
        pronto = True

qtdNaOH = 0
qtdEtOH = 0

inicio = time()
fim =  time()

while fim - inicio <= 3600:
    if qtdNaOH < 30:
        qtdNaOH += 0.5
    if qtdEtOH < 30:
        qtdEtOH += 0.25


    #Vazao dos produtos
    if(qtdEtOH + qtdNaOH <= 1):
        mensagem(qtdEtOH, "ETOH")
        msgBytes =server.recv(2048)
        retirado = float(msgBytes.decode())
        qtdEtOH -= retirado
        if(qtdEtOH < 0):
            qtdEtOH = 0
        mensagem(qtdNaOH, "NAOH")
        msgBytes =server.recv(2048)
        retirado = float(msgBytes.decode())
        qtdNaOH -= retirado
    else:
        if(qtdNaOH > 1 and qtdEtOH < 1):
            mensagem(1, "NAOH")
            msgBytes = server.recv(2048)
            retirado  = float(msgBytes.decode())
            qtdNaOH -= 1
        
        elif(qtdEtOH > 1 and qtdNaOH < 1):
            mensagem(1, "NAOH")
            msgBytes = server.recv(2048)
            retirado  = float(msgBytes.decode())
            qtdNaOH -= retirado
        
        elif(qtdNaOH > 1 and qtdEtOH > 1):
            mensagem(0.5, "NAOH")
            msgBytes = server.recv(2048)
            retirado  = float(msgBytes.decode())
            qtdNaOH -= retirado

            mensagem(0.5, "ETOH")
            msgBytes = server.recv(2048)
            retirado  = float(msgBytes.decode())
            qtdEtOH -= retirado
        
        elif(qtdNaOH < 1 and qtdEtOH < 1):
            mensagem(qtdNaOH / 2, "NAOH")
            msgBytes = server.recv(2048)
            retirado  = float(msgBytes.decode())
            qtdNaOH -= retirado

            mensagem(qtdEtOH / 2, "ETOH")
            msgBytes = server.recv(2048)
            retirado  = float(msgBytes.decode())
            qtdEtOH -= retirado
        
        elif(qtdNaOH== 1):
            mensagem(1, "NAOH")
            retirado  = float(msgBytes.decode())
            qtdEtOH -= retirado

        elif(qtdEtOH == 1):
            mensagem(1, "ETOH")
            retirado  = float(msgBytes.decode())
            qtdEtOH -= retirado



            
        

    msgMonitor = "------\nQuantidades no Tanque de Naoh / Etoh\nNaOH: " + str(qtdNaOH) + "\nEtOH: " + str(qtdEtOH) + "------\n"
    print(msgMonitor)
    sleep(1)