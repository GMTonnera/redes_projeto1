from time import sleep
import socket


HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

clientesConectados = 0
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


jogo = None #instancia do jogo(servidor)

try:
    serverSocket.bind((HOST, PORT))
    serverSocket.listen()
except:
    print(str(socket.error))




clientes = {}
for i in range(4):      
    client, address = serverSocket.accept()
    nome = client.recv(1024).decode("utf-8")
    clientes[i] = (client, nome)
    print(f"conectado: {address[0]} {address[1]}")
    for i in clientes.keys():
        clientes[i][1].sendall(f"fila {clientesConectados}".encode("utf-8"))
         
for i in clientes.keys():
        i[1].sendall("start 0".encode("utf-8"))        

