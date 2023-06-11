from constants import *


class Mensagem:
    def __init__(self, descricao, cor):
        self.__descricao = descricao
        self.__cor = cor

    def get_descricao(self):
        return self.__descricao
    

    def set_descricao(self, descricao):
        self.__descricao = descricao

    
    def get_cor(self):
        return self.__cor
    

    def set_cor(self, cor):
        self.__cor = cor


class CartaJogadaMensagem(Mensagem):
    def __init__(self, jogador, carta):
        super().__init__(f"{jogador.get_nome()} jogou a carta {carta.get_char()}", PRETO_AMARELO)


class GanhadorPartidaMensagem(Mensagem):
    def __init__(self, jogador, num_partida):
        super().__init__(f"{jogador.get_nome()} venceu a partida {num_partida}", PRETO_VERMELHO)


class GanhadorRodadaMenagem(Mensagem):
    def __init__(self, dupla, num_rodada):
        super().__init__(f"{dupla} venceram a rodada {num_rodada}", PRETO_MAGENTA)


class EmpatePartidaMensagem(Mensagem):
    def __init__(self, num_partida):
        super().__init__(f"Partida {num_partida} cangou", PRETO_VERMELHO)


class InicioRodadaMensagem(Mensagem):
    def __init__(self, num_rodada):
        super().__init__(f"Rodada {num_rodada} iniciada", PRETO_MAGENTA)


class PedirTrucoMensagem(Mensagem):
    def __init__(self, jogador):
        super().__init__(f"{jogador.get_nome()} pediu TRUCO", PRETO_VERDE)


class RejeitarTrucoMenagem(Mensagem):
    def __init__(self, jogador):
        super().__init__(f"{jogador.get_nome()} fugiu", PRETO_VERDE)


class AceitarTrucoMensagem(Mensagem):
    def __init__(self, jogador):
        super().__init__(f"{jogador.get_nome()} aceitou", PRETO_VERDE)


class Pedir6Mensagem(Mensagem):
    def __init__(self, jogador):
        super().__init__(f"{jogador.get_nome()} pediu 6", PRETO_VERDE)


class Pedir9Mensagem(Mensagem):
    def __init__(self, jogador):
        super().__init__(f"{jogador.get_nome()} pediu 9", PRETO_VERDE)


class Pedir12Mensagem(Mensagem):
    def __init__(self, jogador):
        super().__init__(f"{jogador.get_nome()} pediu 12", PRETO_VERDE)

