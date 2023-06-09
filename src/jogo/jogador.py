import random

from baralho import Baralho


class Jogador:
    def __init__(self, _id, nome, dupla, pos) -> None:
        self.__id = _id
        self.__nome = nome
        self.__baralho = Baralho(self)
        self.__dupla = dupla
        self.__pos = pos


    def get_id(self):
        return self.__id
    

    def set_id(self, new_id):
        self.__id = new_id

    
    def get_nome(self):
        return self.__nome
    

    def set_nome(self, new_nome):
        self.__nome = new_nome


    def get_baralho(self):
        return self.__baralho
    

    def set_cartas(self, new_baralho):
        self.__baralho = new_baralho


    def get_dupla(self):
        return self.__dupla
    

    def set_dupla(self, new_dupla):
        self.__dupla = new_dupla

    
    def get_pos(self):
        return self.__pos
    

    def set_pos(self, pos):
        self.__pos = pos



    def descartar_carta(self, num):
        return self.__baralho.pop_carta_na_pos(num-1)


    def descartar_carta_random(self):
        return random.randint(49, 48+len(self.__baralho.get_cartas()))


    def __repr__(self) -> str:
        return f"({self.__nome}, id={self.__id})"