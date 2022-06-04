import socket
from time import sleep, time

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

tanques = [0.0,0.0,0.0]


server.sendto("lavagem".encode(), ('localhost', 12000))

pronto = False

while not pronto:
    msgBytes =server.recv(2048)
    if msgBytes.decode() == "pronto":
        pronto = True

tqAtual=0
def updateTanques():
    global tqAtual
    emulsao = 0
    qtdEnviada = 0
    if tqAtual < 2:
        if tanques[tqAtual] == 0:
            pass
        elif tanques[tqAtual] <= 1.5:
            emulsao += tanques[tqAtual] * 0.025
            tanques[tqAtual + 1] += tanques[tqAtual] * 0.975
            tanques[tqAtual] = 0
        else:
            emulsao += 1.5 * 0.025
            tanques[tqAtual + 1] += 1.5 * 0.975
            tanques[tqAtual] -= 1.5
        
        tqAtual += 1
    
    
    else:
        if(tanques[2] > 0):
            
            if tanques[2] <= 1.5:
                qtdEnviada = tanques[2]
                tanques[2] = 0
            else:
                qtdEnviada = 1.5
                tanques[2] -= 1.5
            
        tqAtual = 0
        

    if emulsao > 0:
        server.sendto(("emulsao " + str(emulsao)).encode(), ('localhost', 12000))

        
        
        
    print("lavagem")
    server.sendto(("enviar " + str(qtdEnviada)).encode(), ('localhost', 12000))

    msgMonitor = "------\nQuantidade de mistura nos tanques: \n" + str(tanques[0]) + "\n" + str(tanques[1]) + "\n" +str(tanques[2]) + "\n------\n"
    print(msgMonitor)
    

def receber():
        server.sendto("receber 1".encode(), ('localhost', 12000)) #colocado 1 para o tamanho do split() continuar como 2
        msgBytes = server.recv(2048)
        qtdInput = float(msgBytes.decode())

        if qtdInput > 0:
            tanques[0] += qtdInput * 0.975
            print("------\ntanque de lavagem abastecido,", str(qtdInput),"de mistura recebido\n------")
            server.sendto(("emulsao " + str(qtdInput * 0.025)).encode(), ('localhost', 12000))

        sleep(1)

inicio = time()
fim =  time()

while fim - inicio <= 3600:
    updateTanques()
    receber()

