class Cliente:
    def __init__(self, id=0):
        self.__id = None
        self.__socket = None
        self.__nome = None
        self.__ip = None
        self.__gate = None
        self.__jogador = None


    def get_socket(self):
        return self.__socket


    def set_socket(self, socket):
        self.__socket = socket


    def get_nome(self):
        return self.__nome


    def set_nome(self, nome):
        self.__nome = nome


    def get_ip(self):
        return self.__ip


    def set_ip(self, ip):
        self.__ip = ip


    def connect_server(self, ip_server, gate):
        self.__socket.connect((ip_server, gate))
    

    def send_message(self, message):
        self.__socket.send(message)
    

    def receive_message(self, time):
        return self.__socket.recv(time)
    
    
    def get_jogador(self):
        return self.__jogador
    

    def set_jogador(self, jogador):
        self.__jogador = jogador


    def get_gate(self):
        return self.__gate


    def set_gate(self, gate):
        self.__gate = gate    


    def close_socket(self):
        self.__socket.close()
        self.__socket = None
        self.__nome = None
        self.__ip = None


    def get_id(self):
        return self.__id
    

    def set_id(self, new_id):
        self.__id = new_id

