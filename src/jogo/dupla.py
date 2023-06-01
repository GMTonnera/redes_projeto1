class Dupla:
    def __init__(self) -> None:
        self.__jogador1 = None
        self.__jogador2 = None
        self.__pontos = 0
        self.__nome = ""


    def get_jogador1(self):
        return self.__jogador1


    def set_jogador1(self, new_jogador):
        self.__jogador1 = new_jogador


    def get_jogador2(self):
        return self.__jogador2
    

    def set_jogador2(self, new_jogador):
        self.__jogador2 = new_jogador


    def get_pontos(self):
        return self.__pontos
    

    def set_pontos(self, new_pontos):
        self.__pontos = new_pontos

    
    def add_pontos(self, pts):
        self.__pontos += pts

    
    def make_nome(self):
        self.__nome = f"{self.__jogador1.get_nome()} e {self.__jogador2.get_nome()}"


    def get_nome(self):
        return self.__nome
    

    def set_nome(self, nome):
        self.__nome = nome


    def __repr__(self) -> str:
        return f"(Jogador1={self.__jogador1}, Jogador2={self.__jogador2}, pontos={self.__pontos})"