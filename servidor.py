import socket
from time import time
from codigos import codigo

class Decantador():
    def __init__(self):
        self.qtdTotal = 0.0
        self.tempoDescanso = 0
        self.descanso = False
        self.pendenteLavagem = 0.0
    
    def monitor(self):
        strMonitor = "------\n" + "Decantador\n" + "Quantidade Total: " + str(self.qtdTotal) + "\n"
        if self.descanso:
            strMonitor +="Em descanso\n"
        else:
            strMonitor += "Ativo\n"
        
        strMonitor += "------"

        return strMonitor

        

class Reator():
    def __init__(self):
        self.qtdTotal = 0.0
        self.qtdOleo = 0.0
        self.qtdNaoh= 0.0
        self.qtdEtoh = 0.0
        self.processado = 0.0
        self.ativo = False
        self.nCiclos = 0
        self.clockEnvio = 5
        self.etohdevolvido = 0.0


    def handleEntrada(self, cod, qt): #retorna quantidade transferida para reator
        enviado = 0
        if self.ativo:
            return 0

        if qt == 0:
            enviado = 0
        if cod == codigo("OLEO"):
            if self.qtdOleo > 3:
                enviado = 0
            else:
                if qt + self.qtdOleo > 3:
                    self.qtdOleo += 3 - self.qtdOleo
                    self.qtdTotal += 1.75 - self.qtdNaoh
                    print("enviado " + str(3 - self.qtdOleo) + " oleo para reator")
                    enviado = 3 - self.qtdOleo
                else:
                    self.qtdOleo += qt
                    self.qtdTotal += qt
                    print("enviado " + str(qt) + " oleo para reator")
                    enviado = qt 

        elif cod == codigo("NAOH"):
            if self.qtdNaoh > 1.75:
                enviado = 0
            else:
                if qt + self.qtdNaoh > 1.75:
                    self.qtdNaoh += 1.75 - self.qtdNaoh
                    self.qtdTotal += 1.75 - self.qtdNaoh
                    print("enviado " + str(1.75 - self.qtdNaoh) + " naoh para reator")
                    enviado = 1.75 - self.qtdNaoh
                else:
                    self.qtdNaoh += qt
                    self.qtdTotal += qt
                    print("enviado " + str(qt) + " naoh para reator")
                    enviado = qt 

        elif cod == codigo("ETOH"):
            if self.qtdEtoh > 1.75:
                enviado = -1 * self.etohdevolvido
            else:
                if qt + self.qtdEtoh > 1.75:
                    self.qtdEtoh += 1.75 - self.qtdEtoh
                    self.qtdTotal += 1.75 - self.qtdNaoh
                    print("enviado " + str(1.75 - self.qtdNaoh) + " etoh para reator")
                    enviado = 1.75 - self.qtdEtoh - self.etohdevolvido
                else:
                    self.qtdEtoh += qt
                    self.qtdTotal += qt
                    print("enviado " + str(qt) + " etoh para reator")
                    enviado = qt - self.etohdevolvido
            
            
            self.etohdevolvido = 0
        
        if(self.qtdEtoh >= 1.25 and self.qtdNaoh >= 1.25 and self.qtdOleo >= 2.5):
            print("reator ativado".upper())
            self.ativo = True
            self.nCiclos += 1
        return enviado

    def processar(self):
        if self.ativo:
            self.qtdTotal -= 5
            self.qtdNaoh -= 1.25
            self.qtdEtoh -= 1.25
            self.qtdOleo -= 2.5
            self.processado += 5
            self.ativo = False
            print("reator desativado".upper())
    
    def escoar(self):
        if self.processado == 0:
            return 0
        if self.processado <= 1:
            temp = self.processado
            self.processado = 0
            return temp
        else:
            self.processado -=  1
            return 1
        

reator = Reator()      
decantador = Decantador()        

#Variaveis de controle do sistema
emulsaoTotal = 0
biodieselTotal = 0
perdaSecador = 0
glicerinaTotal = 0
ciclosDecantador = 0


server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

enderecos = dict()
server.bind(('localhost',12000))



while not ({"naetoh", "decantador", "reator", "lavagem", "oleo", "secador"}.issubset(set(enderecos.keys()))):
    bytesMsg, endereco = server.recvfrom(2048)
    resposta = bytesMsg.decode()

    if not resposta in enderecos.keys():
        enderecos[resposta] = endereco
        print(resposta + " entrou")

print("Todos os componentes estão logados")

for end in enderecos.values():
    server.sendto("pronto".encode(), end)

inicio = time()
fim =  time()

while fim - inicio <= 3600:
    bytesMsg, endereco = server.recvfrom(2048)
    resposta = bytesMsg.decode()

    if endereco == enderecos["oleo"]:
        tipoProduto, qtdd = resposta.split()
        server.sendto(str(reator.handleEntrada(tipoProduto, float(qtdd))).encode(), endereco)
    
    elif endereco == enderecos["naetoh"]:
        tipoProduto, qtdd = resposta.split()
        server.sendto(str(reator.handleEntrada(tipoProduto, float(qtdd))).encode(), endereco)
    
    elif endereco == enderecos["reator"]:
        if resposta == "processar":
            reator.processar()
        elif resposta ==  "vazao":
            if not decantador.descanso and decantador.qtdTotal <= 9 and reator.processado > 0:
                decantador.qtdTotal += reator.escoar()
                if(reator.clockEnvio > 0):
                    reator.clockEnvio -= 1
                
                else:
                    decantador.descanso = True
                    decantador.tempoDescanso = 5
                    ciclosDecantador += 1
                    reator.clockEnvio = 5

    elif endereco == enderecos["decantador"]:
        if resposta == "lancar":
            if decantador.descanso:
                decantador.tempoDescanso -= 1
                if decantador.tempoDescanso == 0:
                    decantador.descanso = False
            elif decantador.qtdTotal > 0 and not decantador.descanso:
                decantador.pendenteLavagem = decantador.qtdTotal
                glicerinaTotal += 0.01 * decantador.qtdTotal
                decantador.qtdTotal = 0
        
        elif resposta == "printar":
            server.sendto(decantador.monitor().encode(), endereco)

            
    
    elif endereco == enderecos["secador"]:
        tipo, qtd = resposta.split()

        if(tipo == "saida"):
            biodieselTotal += float(qtd)
        else:
            perdaSecador += float(qtd)
 
    elif endereco == enderecos["lavagem"]:
        tipo, qtd = resposta.split()
        if tipo == "emulsao":
            emulsaoTotal += float(qtd)
        elif tipo == "enviar":
            server.sendto(str(decantador.qtdTotal).encode(), enderecos["secador"])
        elif tipo == "receber":
            server.sendto(str(decantador.pendenteLavagem).encode(), endereco)
            decantador.pendenteLavagem = 0
    
    fim = time()

print("fim de execucao")
print("Emulsao " + str(emulsaoTotal))
print("Biodiesel produzido " + str(biodieselTotal))
print("Perda do secador: " + str(perdaSecador))
print("Glicerina produzida: " + str(glicerinaTotal))
print("Total de ciclos do decantador: " + str(ciclosDecantador))
print("Total de ciclos do reator: " + str(reator.nCiclos))

 
