import socket
import time

from cliente import Cliente

PORTA_SERVIDOR = 1000
IP_SERVIDOR = '127.0.0.1'


def main_cliente():
    cliente = Cliente()
    cliente.set_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    nome = socket.gethostname()
    cliente.set_nome(nome)
    ip = socket.gethostbyname_ex(nome)
    cliente.set_ip(ip[2][0])
    
    print(cliente.get_nome())
    print(cliente.get_ip())
    
    # cliente.connect_server(IP_SERVIDOR, PORTA_SERVIDOR)
    # time.sleep(2)
    # mensagem = cliente.receive_message(1000)
    # print(mensagem)
    # cliente.close_socket()    



if __name__ == "__main__":
    main_cliente()