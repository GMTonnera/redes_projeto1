from concurrent.futures import ThreadPoolExecutor
import time
import socket

# from cliente import Cliente
# from servidor import Servidor



def cliente():
    socketCliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    time.sleep(2)
    socketCliente.connect((ip_servidor[2][0], 4400))
    socketCliente.send(bytes("teste 1 2 3...", "utf-8"))
    msg = socketCliente.recv(1000)
    print("Cliente:", msg)
    socketCliente.close()

threadPool = ThreadPoolExecutor()
threadPool.submit(cliente)

socketServidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
nome_servidor = socket.gethostname()
print(nome_servidor)
ip_servidor = socket.gethostbyname_ex(nome_servidor)
print(ip_servidor)
socketServidor.bind((ip_servidor[2][0], 4400))
print(socketServidor)
socketServidor.listen(1)
(socketParaCliente, enderecoDoCliente) = socketServidor.accept()
print("socket para cliente:",socketParaCliente)
print("endereço do cliente:",enderecoDoCliente)
time.sleep(1)
msgRecebida = socketParaCliente.recv(1000)
print("Servidor:", msgRecebida)
time.sleep(1)
socketParaCliente.send(msgRecebida)
time.sleep(1)
socketServidor.close()

# def cliente():
#     cli = Cliente()
#     time.sleep(2)
#     cli.connect_server(server.get_ip[2][0], server.get_porta())

    


# server = Servidor()