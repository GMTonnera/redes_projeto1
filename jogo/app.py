import time
import random
import socket

from constants import *

from jogo_truco import JogoTruco
from dupla import Dupla
from jogador import Jogador

from mensagem import InicioRodadaMensagem, CartaJogadaMensagem, EmpatePartidaMensagem, GanhadorPartidaMensagem,GanhadorRodadaMenagem 


class App:
    def __init__(self, listaJogadores):        
        # Jogo de Truco
        self.__trucoGame = None

        #Jogadores: lista de tuplas (nome, socket)
        self.__jogadores = listaJogadores

        # Estado do jogo
        self.__state = 0


    def game(self):
        self.criar_jogo()

        while True:
            self.distribuir_cartas()            
            
            #meio gambiarra

            time.sleep(4)
            # Iniciar rodada
            self.__trucoGame.init_rodada()
            rodada = self.__trucoGame.get_rodada_atual()
            
            msg = InicioRodadaMensagem(len(self.__trucoGame.get_rodadas()))
            self.enviarPacoteTodos(f"menssagem {msg.get_cor()} {msg.get_descricao()}")
            
            # Jogar as partidas da rodada
            while rodada.get_dupla_vencedora() is None:
                # Iniciar a partida
                rodada.init_partida()
                partida = rodada.get_partida_atual()
                
                # Desenhar as cartas do jogador1
                #self.draw_cartas_jogador1()
                
                # Adquirir as cartas que cada jogador descartou
                for _ in range(4):
                    jogador = rodada.next_jogador()
                    
                    while True:
                        if jogador == self.__trucoGame.get_dupla1().get_jogador1():
                            # Adquirir a carta que o jogador1 escolheu descartar
                            c = input()
                            
                        else:
                            # Adquirir as cartas dos demais jogadores
                            c = jogador.descartar_carta_random()
                        
                        if self.handle_input(c, jogador, partida):
                            break    
                    

                # Verificar vencedor da partida
                partida.verificar_vencedor()
                self.final_partida_animation()
                if partida.get_vencedor() is None:
                    self.__ledger.add_mensagem(EmpatePartidaMensagem(len(rodada.get_partidas())))
                
                else:
                    self.__ledger.add_mensagem(GanhadorPartidaMensagem(partida.get_vencedor(), len(rodada.get_partidas())))
                
                self.draw_messages()


                # Atualizar fila de jogadores
                rodada.update_fila_jogadores() 

                # Verificar vencedor da rodada
                rodada.verificar_vencedor()
                if rodada.get_dupla_vencedora() is not None:
                    self.__ledger.add_mensagem(GanhadorRodadaMenagem(rodada.get_dupla_vencedora().get_nome(), len(self.__trucoGame.get_rodadas())))             
                
                self.draw_messages()

            # Atualizar fila de jogadores para a próxima rodada
            self.__trucoGame.update_fila_jogadores()

            # Limpar baralho e inicializa-lo de novo
            self.__trucoGame.get_baralho().limpar()
            self.__trucoGame.init_baralho()
            self.__trucoGame.get_baralho().embaralhar()

            # Limpar o baralho dos jogadores
            self.__trucoGame.limpar_baralho_jogadores()

            self.final_rodada_animation()

            c = self.__window.getch()
            

            if c == ord("x"):
                self.__state = -1
                break


    def main(self):
        while True: 
            self.game()    

    

    def criar_jogo(self):
        # Criar instancia do jogo
        self.__trucoGame =  JogoTruco()
        
        # Criar duplas do jogo
        dupla1 = Dupla()
        dupla2 = Dupla()
        
        # Criar jogadores
        jogador1 = Jogador(0, self.__jogadores[0][0], dupla1, (50, 22), self.__jogadores[0][1])
        jogador2 = Jogador(1, self.__jogadores[1][0], dupla1, (50, 14), self.__jogadores[1][1])
        jogador3 = Jogador(2, self.__jogadores[2][0], dupla2, (58, 18), self.__jogadores[2][1])
        jogador4 = Jogador(3, self.__jogadores[3][0], dupla2, (41, 18), self.__jogadores[3][1])

        # Adicionar os jogadores na respectivas duplas
        dupla1.set_jogador1(jogador1)
        dupla1.set_jogador2(jogador2)
        dupla2.set_jogador1(jogador3)
        dupla2.set_jogador2(jogador4)

        # Inicializar o nome das duplas
        dupla1.make_nome()
        dupla2.make_nome()

        # Adicionar as duplas no jogo
        self.__trucoGame.set_dupla1(dupla1)
        self.__trucoGame.set_dupla2(dupla2)

        # Inicializar o baralho
        self.__trucoGame.init_baralho()

        # Inicializar fila de jogadores
        self.__trucoGame.init_fila_jogadores()

        # Embaralhar baralho
        self.__trucoGame.get_baralho().embaralhar()


    def round_menu(self):
        pass


    def enviarPacote(self, mensagem, jogador):
        time.sleep(0.1)
        socket = self.__jogadores[jogador][1]
        socket.sendall(mensagem.encode("utf-8"))

    def enviarPacoteTodos(self, mensagem):
        for i in range(4):
            self.enviarPacote(mensagem, i)
   

    def distribuir_cartas(self):
        deck = self.__trucoGame.get_baralho()
        queue = self.__trucoGame.get_fila_jogadores()
        for i in range(4):
            player = queue.pop(0)
            deck_player = player.get_baralho()
            cartasString = list()
            for _ in range(3):
                card = deck.topo()
                deck_player.add_carta(card.get_char(), card.get_valor())
                cartasString.append(str(card.get_char()))
            #socket = self.__jogadores[i][1]
            #socket.sendall("teste 0".encode("utf-8"))
            self.enviarPacote(f"recebercarta {' '.join(cartasString)}", i)

            queue.append(player)
    




    def descartar_carta_player1_animation(self, carta, num_partidas):
        self.__gameFrame.set_pixel_char(50, 22, carta.get_char())
        self.draw_cartas_jogador1()
        if self.__trucoGame.get_rodada_atual().get_num_partidas() == 1:
            self.__gameFrame.set_pixel_char(52, 27, " ")
            self.__gameFrame.set_pixel_color(52, 27, PRETO_BRANCO)

        elif self.__trucoGame.get_rodada_atual().get_num_partidas() == 2:
            self.__gameFrame.set_pixel_char(50, 27, " ")
            self.__gameFrame.set_pixel_color(50, 27, PRETO_BRANCO)

        else:
            self.__gameFrame.set_pixel_char(48, 27, " ")
            self.__gameFrame.set_pixel_color(48, 27, PRETO_BRANCO)
        
        self.draw_frame()


    def descartar_carta_player2_animation(self, carta):
        self.__gameFrame.set_pixel_char(58, 18, carta.get_char())
        if self.__trucoGame.get_rodada_atual().get_num_partidas() == 1:
            self.__gameFrame.set_pixel_char(67, 20, " ")
            self.__gameFrame.set_pixel_color(67, 20, PRETO_BRANCO)

        elif self.__trucoGame.get_rodada_atual().get_num_partidas() == 2:
            self.__gameFrame.set_pixel_char(67, 18, " ")
            self.__gameFrame.set_pixel_color(67, 18, PRETO_BRANCO)

        else:
            self.__gameFrame.set_pixel_char(67, 16, " ")
            self.__gameFrame.set_pixel_color(67, 16, PRETO_BRANCO)

        self.draw_frame()


    def descartar_carta_player3_animation(self, carta):
        self.__gameFrame.set_pixel_char(50, 14, carta.get_char())
        if self.__trucoGame.get_rodada_atual().get_num_partidas() == 1:
            self.__gameFrame.set_pixel_char(52, 10, " ")
            self.__gameFrame.set_pixel_color(52, 10, PRETO_BRANCO)

        elif self.__trucoGame.get_rodada_atual().get_num_partidas() == 2:
            self.__gameFrame.set_pixel_char(50, 10, " ")
            self.__gameFrame.set_pixel_color(50, 10, PRETO_BRANCO)

        else:
            self.__gameFrame.set_pixel_char(48, 10, " ")
            self.__gameFrame.set_pixel_color(48, 10, PRETO_BRANCO)

        self.draw_frame()


    def descartar_carta_player4_animation(self, carta):
        self.__gameFrame.set_pixel_char(41, 18, carta.get_char())
        if self.__trucoGame.get_rodada_atual().get_num_partidas() == 1:
            self.__gameFrame.set_pixel_char(31, 16, " ")
            self.__gameFrame.set_pixel_color(31, 16, PRETO_BRANCO)

        elif self.__trucoGame.get_rodada_atual().get_num_partidas() == 2:
            self.__gameFrame.set_pixel_char(31, 18, " ")
            self.__gameFrame.set_pixel_color(31, 18, PRETO_BRANCO)

        else:
            self.__gameFrame.set_pixel_char(31, 20, " ")
            self.__gameFrame.set_pixel_color(31, 20, PRETO_BRANCO)

        self.draw_frame()




    def get_truco_game(self):
        return self.__trucoGame
    

    def final_partida_animation(self):
        partida = self.__trucoGame.get_rodada_atual().get_partida_atual()
        # Verificar o vencedor
        if partida.get_vencedor() is not None:
            vencedor = partida.get_vencedor()
            pos = vencedor.get_pos()
            self.__gameFrame.set_pixel_color(pos[0], pos[1], PRETO_VERMELHO)
            self.draw_frame()
            time.sleep(3)
            self.__gameFrame.set_pixel_color(pos[0], pos[1], PRETO_BRANCO)
            self.draw_frame()
        
        else:
            cartas = partida.get_cartas()
            for carta in cartas:
                if carta == cartas[0]:
                    pos = carta.get_baralho().get_dono().get_pos()
                    self.__gameFrame.set_pixel_color(pos[0], pos[1], PRETO_VERMELHO)

            self.draw_frame()
            time.sleep(3)            

            for carta in cartas:
                if carta == cartas[0]:
                    pos = carta.get_baralho().get_dono().get_pos()
                    self.__gameFrame.set_pixel_color(pos[0], pos[1], PRETO_BRANCO)


        self.draw_frame()
        
        # Recolher cartas
        c1 = self.__gameFrame.get_pixel(50, 22).get_char()
        c2 = self.__gameFrame.get_pixel(58, 18).get_char()
        c3 = self.__gameFrame.get_pixel(50, 14).get_char()
        c4 = self.__gameFrame.get_pixel(41, 18).get_char()
        
        ## Recolher carta do player 1
        self.__gameFrame.set_pixel_char(50, 22, " ")
        self.__gameFrame.set_pixel_char(61, 27, c1)
        self.draw_frame()
        time.sleep(0.5)

        ## Recolher carta do player 2
        self.__gameFrame.set_pixel_char(58, 18, " ")
        self.__gameFrame.set_pixel_char(63, 27, c2)
        self.draw_frame()
        time.sleep(0.5)

        ## Recolher carta do player 3
        self.__gameFrame.set_pixel_char(50, 14, " ")
        self.__gameFrame.set_pixel_char(65, 27, c3)
        self.draw_frame()
        time.sleep(0.5)

        ## Recolher carta do player 4
        self.__gameFrame.set_pixel_char(41, 18, " ")
        self.__gameFrame.set_pixel_char(67, 27, c4)
        self.draw_frame()
        time.sleep(0.5)

        ## Juntar cartas
        for i in range(61, 67):
            self.__gameFrame.set_pixel_char(i, 27, " ")
            self.__gameFrame.set_pixel_char(i+1, 27, c1)
            time.sleep(0.1)
            self.draw_frame()
            
        # self.__gameFrame.set_pixel_char(79, 8, " ")
        # self.__gameFrame.set_pixel_char(79, 7, c1)
        # self.draw_frame()
        # time.sleep(0.5)
        # self.__gameFrame.set_pixel_char(79, 7, " ")
        # self.__gameFrame.set_pixel_char(79, 6, c1)
        # self.draw_frame()
        # time.sleep(0.5)
        # self.__gameFrame.set_pixel_char(79, 6, " ")
        # self.__gameFrame.set_pixel_char(79, 5, c1)
        # self.draw_frame()
        # time.sleep(0.5)

        
    def final_rodada_animation(self):
        # Limpar Mesa
        for y in range(10, 28):
            for x in range(31, 69):
                self.__gameFrame.set_pixel_char(x, y, " ")
                self.__gameFrame.set_pixel_color(x, y, PRETO_BRANCO)

        # Colocar o baralho no centro        
        self.__gameFrame.set_pixel_char(50, 18, back_carta)
        self.__gameFrame.set_pixel_color(50, 18, PRETO_CIANO)

        self.draw_frame()

    
 





    def draw_placar(self):
        dupla1_str = f"{self.__trucoGame.get_dupla1().get_nome()}: {self.__trucoGame.get_dupla1().get_pontos()}"
        dupla2_str = f"{self.__trucoGame.get_dupla2().get_nome()}: {self.__trucoGame.get_dupla2().get_pontos()}"

        for i in range(len(dupla1_str)):
            self.__gameFrame.set_pixel_char(i+1, 35, dupla1_str[i])
        
        for i in range(len(dupla2_str)):
            self.__gameFrame.set_pixel_char(i+1, 36, dupla2_str[i])

        self.draw_frame()
        

    def get_input_jogador(self):
        return self.__window.getch()
    

    def handle_input(self, char, jogador, partida):
        if 49 <= char <= 51:
            if 0 < char-48 <= jogador.get_baralho().get_num_cartas():
                # Jogador descarta carta escolhida
                carta = jogador.descartar_carta(char-48)
                # Fazer a aniamacao de descarte
                if jogador == self.__trucoGame.get_dupla1().get_jogador1():
                    self.descartar_carta_player1_animation(carta)
                elif jogador == self.__trucoGame.get_dupla2().get_jogador1():
                    self.descartar_carta_player2_animation(carta)
                elif jogador == self.__trucoGame.get_dupla1().get_jogador2():
                    self.descartar_carta_player3_animation(carta)
                elif jogador == self.__trucoGame.get_dupla2().get_jogador2():
                    self.descartar_carta_player4_animation(carta)
                
                # Adicionar a carta na partida
                partida.add_carta(carta)

                # Criar mensagem de carta descartada
                self.__ledger.add_mensagem(CartaJogadaMensagem(jogador, carta))
                self.draw_messages()

                return True
        
        # Pedir 
        elif char == ord('t'):
            partida.get_rodada().set_estado(1, jogador)
            
        
        # Aceitar 
        elif char == ord('a'):
            partida.get_rodada().set_estado(2, jogador)
            
        # Fugir  
        elif char == ord('f'):
            partida.get_rodada().set_estado(4, jogador)
            estado =  partida.get_rodada().get_estado()
            
        # Aumentar
        elif char == ord('g'):
            partida.get_rodada().set_estado(3, jogador)
            

        return False
        



            