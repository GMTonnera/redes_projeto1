import socket
import app


HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

clientesConectados = 1
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



try:
    serverSocket.bind((HOST, PORT))
    serverSocket.listen()
except:
    print(str(socket.error))




clientes = []
for i in range(4):      
    client, address = serverSocket.accept()
    nome = client.recv(1024).decode("utf-8")
    clientes.append((nome, client))
    print(f"conectado: {address[0]} {address[1]}")
    for i in clientes:
        i[1].sendall(f"fila {clientesConectados}".encode("utf-8"))
    clientesConectados += 1


for i in range(len(clientes)):
        clientes[i][1].sendall(f"start {i} {clientes[0][0]} {clientes[1][0]} {clientes[2][0]} {clientes[3][0]}".encode("utf-8"))
        clientes[i][1].recv(1024).decode("utf-8")

print("start")
jogo = app.App(clientes)
jogo.main()

