from baralho import Baralho
from rodada import Rodada
from unicode_chars import *



class JogoTruco:
    def __init__(self) -> None:
        self.__dupla1 = None
        self.__dupla2 = None
        self.__baralho = Baralho(self)
        self.__rodadas = [] 
        self.__fila_jogadores = []
    

    def get_dupla1(self):
        return self.__dupla1
    

    def set_dupla1(self, new_dupla):
        self.__dupla1 = new_dupla


    def get_dupla2(self):
        return self.__dupla2
    

    def set_dupla2(self, new_dupla):
        self.__dupla2 = new_dupla

    
    def get_baralho(self):
        return self.__baralho
    

    def set_cartas(self, new_baralho):
        self.__baralho = new_baralho


    def get_rodadas(self):
        return self.__rodadas
    

    def get_rodada_atual(self):
        return self.__rodadas[-1]


    def set_rodadas(self, new_rodadas):
        self.__rodadas = new_rodadas
    

    def get_fila_jogadores(self):
        return self.__fila_jogadores
    

    def set_fila_jogadores(self, new_fila):
        self.__fila_jogadores = new_fila


    def init_rodada(self):
        self.__rodadas.append(Rodada(len(self.__rodadas), self, self.__fila_jogadores.copy()))


    def init_baralho(self):
        self.__baralho.add_carta(valete_espadas, 1)
        self.__baralho.add_carta(valete_paus, 1)
        self.__baralho.add_carta(valete_ouros, 1)
        self.__baralho.add_carta(valete_copas, 1)

        self.__baralho.add_carta(dama_espadas, 2)
        self.__baralho.add_carta(dama_paus, 2)
        self.__baralho.add_carta(dama_ouros, 2)
        self.__baralho.add_carta(dama_copas, 2)

        self.__baralho.add_carta(rei_espadas, 3)
        self.__baralho.add_carta(rei_paus, 3)
        self.__baralho.add_carta(rei_ouros, 3)
        self.__baralho.add_carta(rei_copas, 3)

        self.__baralho.add_carta(as_paus, 4)
        self.__baralho.add_carta(as_ouros, 4)
        self.__baralho.add_carta(as_copas, 4)

        self.__baralho.add_carta(dois_espadas, 5)
        self.__baralho.add_carta(dois_paus, 5)
        self.__baralho.add_carta(dois_ouros, 5)
        self.__baralho.add_carta(dois_copas, 5)

        self.__baralho.add_carta(tres_espadas, 6)
        self.__baralho.add_carta(tres_paus, 6)
        self.__baralho.add_carta(tres_ouros, 6)
        self.__baralho.add_carta(tres_copas, 6)

        self.__baralho.add_carta(coringa, 7)
        self.__baralho.add_carta(sete_ouros, 8)
        self.__baralho.add_carta(as_espadas, 9)
        self.__baralho.add_carta(sete_copas, 10)
        self.__baralho.add_carta(quatro_paus, 11)


    def init_fila_jogadores(self):
        self.__fila_jogadores.append(self.__dupla1.get_jogador1())
        self.__fila_jogadores.append(self.__dupla2.get_jogador1())
        self.__fila_jogadores.append(self.__dupla1.get_jogador2())
        self.__fila_jogadores.append(self.__dupla2.get_jogador2())


    def update_fila_jogadores(self):
        last = self.__fila_jogadores.pop(0)
        for _ in range(3):    
            j = self.__fila_jogadores.pop(0)
            self.__fila_jogadores.append(j)
        
        self.__fila_jogadores.append(last)

    
    def limpar_baralho_jogadores(self):
        self.__dupla1.get_jogador1().get_baralho().limpar()
        self.__dupla1.get_jogador2().get_baralho().limpar()
        self.__dupla2.get_jogador1().get_baralho().limpar()
        self.__dupla2.get_jogador2().get_baralho().limpar()

