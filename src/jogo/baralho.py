from random import shuffle


from carta import Carta


class Baralho:
    def __init__(self, dono):
        self.__dono = dono
        self.__cartas = []
    

    def get_dono(self):
        return self.__dono
    

    def set_dono(self, new_dono):
        self.__dono = new_dono


    def get_cartas(self):
        return self.__cartas
    

    def set_cartas(self, new_cartas):
        self.__cartas = new_cartas


    def add_carta(self, char, valor):
        self.__cartas.append(Carta(char, valor, self))


    def remover_carta(self, char):
        for carta in self.__cartas:
            if carta.get_char() == char:
                self.__cartas.remove(carta)


    def topo(self):
        return self.__cartas.pop(0)


    def embaralhar(self):
        shuffle(self.__cartas)


    def limpar(self):
        self.__cartas.clear()


    def pop_carta_na_pos(self, idx):
        return self.__cartas.pop(idx)
    

    def get_num_cartas(self):
        return len(self.__cartas)