class Partida:
    def __init__(self, rodada):
        self.__cartas = []
        self.__vencedor = None
        self.__rodada = rodada


    def get_cartas(self):
        return self.__cartas
    

    def set_cartas(self, cartas):
        self.__cartas = cartas


    def get_vencedor(self):
        return self.__vencedor


    def set_vencedor(self, vencedor):
        self.__vencedor = vencedor 


    def get_rodada(self):
        return self.__rodada


    def set_rodada(self, rodada):
        self.__rodada = rodada


    def add_carta(self, carta):
        self.__cartas.append(carta)


    def verificar_vencedor(self):
        self.__cartas.sort(reverse=True)

        if self.__cartas[0] != self.__cartas[1]:
            self.__vencedor = self.__cartas[0].get_baralho().get_dono()
            return True
        else:
            if self.__cartas[0].get_baralho().get_dono().get_dupla() == self.__cartas[1].get_baralho().get_dono().get_dupla():
                self.__vencedor = self.__cartas[1].get_baralho().get_dono()
                return True

        return False


    def get_carta_vencedora(self):
        return self.__cartas[0]

