import socket
from threading import Thread


from cliente.cliente import Cliente
from jogo.jogo_truco import JogoTruco


class Servidor:
    def __init__(self, porta, n_max):
        # Inicializar socket
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Adquirir nome do host
        self.__nome = socket.gethostname()
        # Adquirir ip do host
        self.__ip = socket.gethostbyname_ex(self.__nome)
        # Numero maximo de conexoes simultaneas
        self.__n_max = n_max
        # Porta
        self.__porta = porta
        # Thread para escuta de novas conexoes
        self.__thread_escuta = Thread(target=self.run_thread_escuta)
        # Jogo de truco
        self.__jogoTruco = JogoTruco()
        # Clientes
        self.__clientes = []

        print(self.__ip)
        # Inicializar porta
        self.__socket.bind((self.__ip[2][0], porta))
        # Configurar numero maximo de conexoes
        self.__socket.listen(n_max)


    def run_thread_escuta(self):
        while len(self.__clientes) < 4:
            # Thread aguarda por novas conexoes
            try:
                (novo_socketCliente, endereco_cliente) = self.__socket.accept()
                print("Novo cliente conectado!")
                c = Cliente(len(self.__clientes))
                c.set_socket(novo_socketCliente)
                c.set_ip(endereco_cliente[0])
                c.set_gate(endereco_cliente[1])
                self.__clientes.append(c)

            except OSError:
                break
            
            
    
    def run_tread_jogo(self):
        pass



    def get_ip(self):
        return self.__ip
    

    def get_porta(self):
        return self.__porta()
    

    def run_thread_cliente(self):
        mensagem = self.__socket.recv()