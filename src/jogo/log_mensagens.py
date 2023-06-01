class LedgerMessages:
    def __init__(self, n_max):
        self.__mensagens = []
        self.__num_max_messagens = n_max


    def add_mensagem(self, mensagem):
        if len(self.__mensagens) == self.__num_max_messagens:
            self.__mensagens.pop(-1)
        self.__mensagens.insert(0, mensagem)


    def get_mensagens(self):
        return self.__mensagens
    

    def set_mensagens(self, mensagens):
        self.__mensagens = mensagens


    def get_num_max_mensagens(self):
        return self.__num_max_messagens
    

    def set_num_max_mensagen(self, num_max):
        self.__num_max_messagens = num_max