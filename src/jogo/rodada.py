from partida import Partida


class Rodada:
    def __init__(self, num, jogo, fila):
        self.__num = num
        self.__jogo = jogo
        self.__pontos = 1
        self.__partidas = []
        self.__dupla_vencedora = None
        self.__estado = 0
        self.__fila_jogadores = fila
        self.__jogadores = []
        self.__g = 1
        self.__pediu_truco = None
        
    
    def get_num(self):
        return self.__num
    

    def set_num(self, new_num):
        self.__num = new_num


    def get_jogo(self):
        return self.__jogo
    

    def set_jogo(self, new_jogo):
        self.__jogo = new_jogo


    def get_pontos(self):
        return self.__pontos
    

    def set_pontos(self, new_pontos):
        self.__pontos = new_pontos


    def get_partidas(self):
        return self.__partidas
    

    def get_partida_atual(self):
        return self.__partidas[-1]


    def set_partidas(self, new_partidas):
        self.__partidas = new_partidas


    def get_dupla_vencedora(self):
        return self.__dupla_vencedora
    

    def set_dupla_vencedora(self, dupla):
        self.__dupla_vencedora = dupla


    def get_estado(self):
        return self.__estado
    

    def set_estado(self, new_estado, jogador):
        self.__estado = new_estado
        
        if self.__estado == 1:
            self.__pediu_truco = jogador.get_dupla()

        elif self.__estado == 2:
            self.__pontos = 3

        elif self.__estado == 3:
            self.__g += 1
            self.__pontos = 3*self.__g 
            self.__pediu_truco = jogador.get_dupla()
            
        elif self.__estado == 4:
            if self.__g > 1:
                self.__pontos -= 3
            self.__pediu_truco.add_pontos(self.__pontos)
            self.__dupla_vencedora = self.__pediu_truco


    def next_jogador(self):
        jogador = self.__fila_jogadores.pop(0)
        self.__jogadores.append(jogador)
        return jogador


    def verificar_vencedor(self):
        if self.__dupla_vencedora is None:
            if len(self.__partidas) == 2:
                if self.__partidas[0].get_vencedor() is None:
                    self.__dupla_vencedora = self.__partidas[1].get_vencedor().get_dupla()  
                    self.__dupla_vencedora.add_pontos(self.__pontos)
                    return True
                
                else:
                    if self.__partidas[1].get_vencedor() is None:
                        self.__dupla_vencedora = self.__partidas[0].get_vencedor().get_dupla()
                        self.__dupla_vencedora.add_pontos(self.__pontos)
                        return True
                    else:
                        if self.__partidas[0].get_vencedor() == self.__partidas[1].get_vencedor():
                            self.__dupla_vencedora = self.__partidas[0].get_vencedor().get_dupla()
                            self.__dupla_vencedora.add_pontos(self.__pontos)
                            return True
                        else:
                            if self.__partidas[0].get_vencedor().get_dupla() == self.__partidas[1].get_vencedor().get_dupla():
                                self.__dupla_vencedora = self.__partidas[0].get_vencedor().get_dupla()
                                self.__dupla_vencedora.add_pontos(self.__pontos)
                                return True
                

            elif len(self.__partidas) == 3:
                if self.__partidas[-1].get_vencedor() is None:
                    self.__dupla_vencedora = self.__partidas[0].get_vencedor().get_dupla()
                    self.__dupla_vencedora.add_pontos(self.__pontos)
                    return True
                else:
                    d1 = 0
                    d2 = 0
                    for partida in self.__partidas:
                        if partida.get_vencedor() in (self.__jogo.get_dupla1().get_jogador1(), self.__jogo.get_dupla1().get_jogador2()):
                            d1 += 1
                        else:
                            d2 += 1
                    
                    if d1 > d2:
                        self.__dupla_vencedora = self.__jogo.get_dupla1()
                        self.__dupla_vencedora.add_pontos(self.__pontos)
                        return True
                    else:
                        self.__dupla_vencedora = self.__jogo.get_dupla2()
                        self.__dupla_vencedora.add_pontos(self.__pontos)
                        return True
            else:
                return False
        
        else:
            return True


    def init_partida(self):
        self.__partidas.append(Partida(self))

    
    def get_num_partidas(self):
        return len(self.__partidas)
    

    def update_fila_jogadores(self):
        if self.__partidas[-1].get_vencedor() is None:
            idx = self.__jogadores.index(self.__partidas[-1].get_cartas()[1].get_baralho().get_dono())

        else:
            idx = self.__jogadores.index(self.__partidas[-1].get_vencedor())
        
        for jogador in self.__jogadores[idx:] + self.__jogadores[:idx]:
            self.__fila_jogadores.append(jogador)
        
        self.__jogadores = []

    
    def get_fila_jogadores(self):
        return self.__fila_jogadores















