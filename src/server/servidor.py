import socket
from threading import Thread
import json
import time


from cliente.cliente import Cliente
from protocolo.mensagem_protocolo import *
# from jogo.jogo_truco import JogoTruco


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
        # self.__jogoTruco = JogoTruco()
        # Clientes
        self.__clientes = []
        # Thread de set up do jogo
        self.__setup_thread = Thread(target=self.run_tread_setup_jogo)
        # Fila de Clientes
        self.__fila_clientes = []


        # Inicializar porta
        self.__socket.bind((self.__ip[2][0], porta))
        # Configurar numero maximo de conexoes
        self.__socket.listen(n_max)
        
        self.__thread_escuta.run()
        self.__setup_thread.run()


    def run_thread_escuta(self):
        print("Iniciando thread de escuta!")
        time.sleep(2)
        while len(self.__clientes) < self.__n_max:
            # Thread aguarda por novas conexoes
            try:
                (novo_socketCliente, endereco_cliente) = self.__socket.accept()
                print("Novo cliente conectado!")
                c = Cliente(len(self.__clientes))
                c.set_socket(novo_socketCliente)
                c.set_ip(endereco_cliente[0])
                c.set_gate(endereco_cliente[1])
                self.__clientes.append(c)
                c.get_socket().send(bytes(f"Conexao com o Cliente {c.get_id()} foi aceita!", "utf-8"))

            except OSError:
                break
        

    
    def run_tread_setup_jogo(self):
        print("Iniciando thread de set up do jogo")
        while len(self.__fila_clientes) < 4:
            for cliente in self.__clientes:
                try:
                    mensagem = cliente.get_socket().recv(1000)
                    self.handle_mensagens(json.loads(mensagem), cliente)
                    time.sleep(2)
                except:
                    continue

                


    def get_ip(self):
        return self.__ip
    

    def get_porta(self):
        return self.__porta()
    

    def run_thread_cliente(self):
        mensagem = self.__socket.recv()


    def handle_mensagens(self, mensagem, cliente):
        if mensagem["Tipo"] == "Solicitação":
            if mensagem["Ação"] == "Entrar na fila":
                cliente.get_socket().send(MensagemRespostaEntrarFila().encode_menssagem())
                self.__fila_clientes.append(cliente)
                print(f"Adicionado cliente {cliente.get_id()} na fila")
                print("Fila de clientes:", self.__fila_clientes)
