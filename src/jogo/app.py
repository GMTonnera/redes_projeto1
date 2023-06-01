import curses
import time
import random

from constants import *
from screens import MENU_SCREEN, GAME_SCREEN, QUEUE_SCREEN
from frame import Frame
from jogo_truco import JogoTruco
from dupla import Dupla
from jogador import Jogador
from unicode_chars import *
from log_mensagens import LedgerMessages
from mensagem import InicioRodadaMensagem, VezJogarMensagem, CartaJogadaMensagem, EmpatePartidaMensagem, GanhadorPartidaMensagem,GanhadorRodadaMenagem 


class App:
    def __init__(self):
        # Janela
        self.__window = curses.initscr()
        
        # Frame do jogo
        self.__gameFrame = Frame(FRAME_WIDTH, FRAME_HEIGHT)
        
        # Frame do menu
        self.__menuFrame = Frame(FRAME_WIDTH, FRAME_HEIGHT)
        
        # Frame da fila
        self.__queueFrame = Frame(FRAME_WIDTH, FRAME_HEIGHT)
        
        # Estado do jogo
        self.__state = 0
        
        # Jogo de Truco
        self.__trucoGame = None
        
        # Ledger de Mensagens
        self.__ledger = LedgerMessages(36)

        # Inicializar o frame da fila
        self.__queueFrame.set_pixels(QUEUE_SCREEN)

        # Inilizar o frame de menu
        self.__menuFrame.set_pixels(MENU_SCREEN)

        # Inicializar o frame do jogo
        self.__gameFrame.set_pixels(GAME_SCREEN)

        


    def menu(self):
        while True:
            self.__window.clear()
            self.draw_frame()
            c = self.__window.getch()

            if c == ord("\n"):
                self.__state = 1
                break
            
            elif c == ord("x"):
                self.__state = -1
                break


    def queue(self):
        while True:
            self.__window.clear()
            self.draw_frame()
            c = self.__window.getch()

            if c == ord("\n"):
                self.__state = 2
                break
            
            elif c == ord("x"):
                self.__state = 0
                break


    def game(self):
        self.criar_jogo()

        while True:
            self.__window.clear()
            self.draw_frame()

            # Atualizar o placa
            self.draw_placar()

            # Distribui as cartas para os 4 jogadores
            self.distribuir_cartas()            

            # Iniciar rodada
            self.__trucoGame.init_rodada()
            rodada = self.__trucoGame.get_rodada_atual()
            self.__ledger.add_mensagem(InicioRodadaMensagem(len(self.__trucoGame.get_rodadas())))
            self.draw_messages()

            # Jogar as partidas da rodada
            while rodada.get_dupla_vencedora() is None:
                # Iniciar a partida
                rodada.init_partida()
                partida = rodada.get_partida_atual()
                
                # Desenhar as cartas do jogador1
                self.draw_cartas_jogador1()
                
                # Adquirir as cartas que cada jogador descartou
                for _ in range(4):
                    jogador = rodada.next_jogador()
                    if jogador == self.__trucoGame.get_dupla1().get_jogador1():
                        # Adquirir a carta que o jogador1 escolheu descartar
                        c = self.get_input_jogador()
                        
                    else:
                        # Adquirir as cartas dos demais jogadores
                        c = jogador.descartar_carta_random()
                    
                    self.handle_input(c, jogador, partida)
                    

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
        # Setar as configuraçoes do terminal
        curses.start_color()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        
        self.init_pares_cores()

        # Main loop
        while True: 
            if self.__state == -1:
                break            
            elif self.__state == 0:
                self.menu()
            elif self.__state == 1:
                self.queue()
            elif self.__state == 2:
                self.game()    
        
        # Resetar configuracoes do terminal
        curses.echo()
        curses.nocbreak()

        # Fechar janela
        curses.endwin()    


    def draw_frame(self):
        for y in range(FRAME_HEIGHT):
            for x in range(FRAME_WIDTH):
                try:
                    if self.__state == 0:
                        self.__window.addch(y, x, self.__menuFrame.get_pixel(x, y).get_char(), curses.color_pair(self.__menuFrame.get_pixel(x, y).get_color()))

                    elif self.__state == 1:
                        self.__window.addch(y, x, self.__queueFrame.get_pixel(x, y).get_char(), curses.color_pair(self.__queueFrame.get_pixel(x, y).get_color()))
                        
                    elif self.__state == 2:
                        self.__window.addch(y, x, self.__gameFrame.get_pixel(x, y).get_char(), curses.color_pair(self.__gameFrame.get_pixel(x, y).get_color()))
                    
                except:
                    pass

        self.__window.refresh()


    def criar_jogo(self):
        # Criar instancia do jogo
        self.__trucoGame =  JogoTruco()
        
        # Criar duplas do jogo
        dupla1 = Dupla()
        dupla2 = Dupla()
        
        # Criar jogadores
        jogador1 = Jogador(0, "Gustavo", dupla1, (50, 22))
        jogador2 = Jogador(1, "Bernardo", dupla1, (50, 14))
        jogador3 = Jogador(2, "Amaral", dupla2, (58, 18))
        jogador4 = Jogador(3, "Vinicius", dupla2, (41, 18))

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


    def entregar_carta_animation1(self):
        for i in range(3):
            self.__gameFrame.set_pixel_char(50, 19, back_carta)
            self.__gameFrame.set_pixel_color(50, 19, PRETO_CIANO)
            
            self.draw_frame()
            time.sleep(0.1)

            for j in range(19, 26):
                self.__gameFrame.set_pixel_char(50, j, " ")
                self.__gameFrame.set_pixel_color(50, j, PRETO_BRANCO)
                self.__gameFrame.set_pixel_char(50, j+1, back_carta)
                self.__gameFrame.set_pixel_color(50, j+1, PRETO_CIANO)
                self.draw_frame()
                time.sleep(0.1)
            
            if i == 0:
                self.__gameFrame.set_pixel_char(50, 26, " ")
                self.__gameFrame.set_pixel_color(50, 26, PRETO_BRANCO)
                self.__gameFrame.set_pixel_char(49, 26, back_carta)
                self.__gameFrame.set_pixel_color(49, 26, PRETO_CIANO)
                self.draw_frame()
                time.sleep(0.1)
                
                self.__gameFrame.set_pixel_char(49, 26, " ")
                self.__gameFrame.set_pixel_color(49, 26, PRETO_BRANCO)
                self.__gameFrame.set_pixel_char(48, 26, back_carta)
                self.__gameFrame.set_pixel_color(48, 26, PRETO_CIANO)
                self.draw_frame()
                time.sleep(0.1)

                self.__gameFrame.set_pixel_char(48, 26, " ")
                self.__gameFrame.set_pixel_color(48, 26, PRETO_BRANCO)
                self.__gameFrame.set_pixel_char(48, 27, back_carta)
                self.__gameFrame.set_pixel_color(48, 27, PRETO_CIANO)
                self.draw_frame()
                time.sleep(0.1)
            
            elif i == 1:
                self.__gameFrame.set_pixel_char(50, 26, " ")
                self.__gameFrame.set_pixel_color(50, 26, PRETO_BRANCO)
                self.__gameFrame.set_pixel_char(51, 26, back_carta)
                self.__gameFrame.set_pixel_color(51, 26, PRETO_CIANO)
                self.draw_frame()
                time.sleep(0.1)
                
                self.__gameFrame.set_pixel_char(51, 26, " ")
                self.__gameFrame.set_pixel_color(51, 26, PRETO_BRANCO)
                self.__gameFrame.set_pixel_char(52, 26, back_carta)
                self.__gameFrame.set_pixel_color(52, 26, PRETO_CIANO)
                self.draw_frame()
                time.sleep(0.1)

                self.__gameFrame.set_pixel_char(52, 26, " ")
                self.__gameFrame.set_pixel_color(52, 26, PRETO_BRANCO)
                self.__gameFrame.set_pixel_char(52, 27, back_carta)
                self.__gameFrame.set_pixel_color(52, 27, PRETO_CIANO)
                self.draw_frame()
                time.sleep(0.1)
            
            elif i == 2:
                self.__gameFrame.set_pixel_char(50, 26, " ")
                self.__gameFrame.set_pixel_color(50, 26, PRETO_BRANCO)
                self.__gameFrame.set_pixel_char(50, 27, back_carta)
                self.__gameFrame.set_pixel_color(50, 27, PRETO_CIANO)
                self.draw_frame()
                time.sleep(0.1)
            

    def entregar_carta_animation2(self):
        for i in range(3):
            self.__gameFrame.set_pixel_char(51, 18, back_carta)
            self.__gameFrame.set_pixel_color(51, 18, PRETO_CIANO)
            self.draw_frame()
            time.sleep(0.05)

            for j in range(51, 66):
                self.__gameFrame.set_pixel_char(j, 18, " ")
                self.__gameFrame.set_pixel_color(j, 18, PRETO_BRANCO)
                self.__gameFrame.set_pixel_char(j+1, 18, back_carta)
                self.__gameFrame.set_pixel_color(j+1, 18, PRETO_CIANO)
                self.draw_frame()
                time.sleep(0.05)
            
            if i == 0:
                self.__gameFrame.set_pixel_char(66, 18, " ")
                self.__gameFrame.set_pixel_color(66, 18, PRETO_BRANCO)
                self.__gameFrame.set_pixel_char(66, 19, back_carta)
                self.__gameFrame.set_pixel_color(66, 19, PRETO_CIANO)
                self.draw_frame()
                time.sleep(0.05)
                
                self.__gameFrame.set_pixel_char(66, 19, " ")
                self.__gameFrame.set_pixel_color(66, 19, PRETO_BRANCO)
                self.__gameFrame.set_pixel_char(66, 20, back_carta)
                self.__gameFrame.set_pixel_color(66, 20, PRETO_CIANO)
                self.draw_frame()
                time.sleep(0.05)

                self.__gameFrame.set_pixel_char(66, 20, " ")
                self.__gameFrame.set_pixel_color(66, 20, PRETO_BRANCO)
                self.__gameFrame.set_pixel_char(67, 20, back_carta)
                self.__gameFrame.set_pixel_color(67, 20, PRETO_CIANO)
                self.draw_frame()
                time.sleep(0.05)
            
            elif i == 1:
                self.__gameFrame.set_pixel_char(66, 18, " ")
                self.__gameFrame.set_pixel_color(66, 18, PRETO_BRANCO)
                self.__gameFrame.set_pixel_char(66, 17, back_carta)
                self.__gameFrame.set_pixel_color(66, 17, PRETO_CIANO)
                self.draw_frame()
                time.sleep(0.05)
                
                self.__gameFrame.set_pixel_char(66, 17, " ")
                self.__gameFrame.set_pixel_color(66, 17, PRETO_BRANCO)
                self.__gameFrame.set_pixel_char(66, 16, back_carta)
                self.__gameFrame.set_pixel_color(66, 16, PRETO_CIANO)
                self.draw_frame()
                time.sleep(0.05)

                self.__gameFrame.set_pixel_char(66, 16, " ")
                self.__gameFrame.set_pixel_color(66, 16, PRETO_BRANCO)
                self.__gameFrame.set_pixel_char(67, 16, back_carta)
                self.__gameFrame.set_pixel_color(67, 16, PRETO_CIANO)
                self.draw_frame()
                time.sleep(0.05)
            
            elif i == 2:
                self.__gameFrame.set_pixel_char(66, 18, " ")
                self.__gameFrame.set_pixel_color(66, 18, PRETO_BRANCO)
                self.__gameFrame.set_pixel_char(67, 18, back_carta)
                self.__gameFrame.set_pixel_color(67, 18, PRETO_CIANO)
                self.draw_frame()
                time.sleep(0.05)
            
    
    def entregar_carta_animation3(self):
        for i in range(3):
            self.__gameFrame.set_pixel_char(50, 17, back_carta)
            self.__gameFrame.set_pixel_color(50, 17, PRETO_CIANO)
            self.draw_frame()
            time.sleep(0.1)

            for j in range(17, 11, -1):
                self.__gameFrame.set_pixel_char(50, j, " ")
                self.__gameFrame.set_pixel_color(50, j, PRETO_BRANCO)
                self.__gameFrame.set_pixel_char(50, j-1, back_carta)
                self.__gameFrame.set_pixel_color(50, j-1, PRETO_CIANO)
                self.draw_frame()
                time.sleep(0.1)
            
            if i == 0:
                self.__gameFrame.set_pixel_char(50, 11, " ")
                self.__gameFrame.set_pixel_color(50, 11, PRETO_BRANCO)
                self.__gameFrame.set_pixel_char(51, 11, back_carta)
                self.__gameFrame.set_pixel_color(51, 11, PRETO_CIANO)
                self.draw_frame()
                time.sleep(0.1)
                
                self.__gameFrame.set_pixel_char(51, 11, " ")
                self.__gameFrame.set_pixel_color(51, 11, PRETO_BRANCO)
                self.__gameFrame.set_pixel_char(52, 11, back_carta)
                self.__gameFrame.set_pixel_color(52, 11, PRETO_CIANO)
                self.draw_frame()
                time.sleep(0.1)

                self.__gameFrame.set_pixel_char(52, 11, " ")
                self.__gameFrame.set_pixel_color(52, 11, PRETO_BRANCO)
                self.__gameFrame.set_pixel_char(52, 10, back_carta)
                self.__gameFrame.set_pixel_color(52, 10, PRETO_CIANO)
                self.draw_frame()
                time.sleep(0.1)
            
            elif i == 1:
                self.__gameFrame.set_pixel_char(50, 11, " ")
                self.__gameFrame.set_pixel_color(50, 11, PRETO_BRANCO)
                self.__gameFrame.set_pixel_char(49, 11, back_carta)
                self.__gameFrame.set_pixel_color(49, 11, PRETO_CIANO)
                self.draw_frame()
                time.sleep(0.1)
                
                self.__gameFrame.set_pixel_char(49, 11, " ")
                self.__gameFrame.set_pixel_color(49, 11, PRETO_BRANCO)
                self.__gameFrame.set_pixel_char(48, 11, back_carta)
                self.__gameFrame.set_pixel_color(48, 11, PRETO_CIANO)
                self.draw_frame()
                time.sleep(0.1)

                self.__gameFrame.set_pixel_char(48, 11, " ")
                self.__gameFrame.set_pixel_color(48, 11, PRETO_BRANCO)
                self.__gameFrame.set_pixel_char(48, 10, back_carta)
                self.__gameFrame.set_pixel_color(48, 10, PRETO_CIANO)
                self.draw_frame()
                time.sleep(0.1)
            
            elif i == 2:
                self.__gameFrame.set_pixel_char(50, 11, " ")
                self.__gameFrame.set_pixel_color(50, 11, PRETO_BRANCO)
                self.__gameFrame.set_pixel_char(50, 10, back_carta)
                self.__gameFrame.set_pixel_color(50, 10, PRETO_CIANO)
                self.draw_frame()
                time.sleep(0.1)
            
    
    def entregar_carta_animation4(self):
        for i in range(3):
            self.__gameFrame.set_pixel_char(49, 18, back_carta)
            self.__gameFrame.set_pixel_color(49, 18, PRETO_BRANCO)
            self.draw_frame()
            time.sleep(0.05)

            for j in range(49, 32, -1):
                self.__gameFrame.set_pixel_char(j, 18, " ")
                self.__gameFrame.set_pixel_color(j, 18, PRETO_BRANCO)
                self.__gameFrame.set_pixel_char(j-1, 18, back_carta)
                self.__gameFrame.set_pixel_color(j-1, 18, PRETO_CIANO)
                self.draw_frame()
                time.sleep(0.05)
            
            if i == 0:
                self.__gameFrame.set_pixel_char(32, 18, " ")
                self.__gameFrame.set_pixel_color(32, 18, PRETO_BRANCO)
                self.__gameFrame.set_pixel_char(32, 17, back_carta)
                self.__gameFrame.set_pixel_color(32, 17, PRETO_CIANO)
                self.draw_frame()
                time.sleep(0.05)
                
                self.__gameFrame.set_pixel_char(32, 17, " ")
                self.__gameFrame.set_pixel_color(32, 17, PRETO_BRANCO)
                self.__gameFrame.set_pixel_char(32, 16, back_carta)
                self.__gameFrame.set_pixel_color(32, 16, PRETO_CIANO)
                self.draw_frame()
                time.sleep(0.05)

                self.__gameFrame.set_pixel_char(32, 16, " ")
                self.__gameFrame.set_pixel_color(32, 16, PRETO_BRANCO)
                self.__gameFrame.set_pixel_char(31, 16, back_carta)
                self.__gameFrame.set_pixel_color(31, 16, PRETO_CIANO)
                self.draw_frame()
                time.sleep(0.05)
    
            elif i == 1:
                self.__gameFrame.set_pixel_char(32, 18, " ")
                self.__gameFrame.set_pixel_color(32, 18, PRETO_BRANCO)
                self.__gameFrame.set_pixel_char(32, 19, back_carta)
                self.__gameFrame.set_pixel_color(32, 19, PRETO_CIANO)
                self.draw_frame()
                time.sleep(0.05)
                
                self.__gameFrame.set_pixel_char(32, 19, " ")
                self.__gameFrame.set_pixel_color(32, 19, PRETO_BRANCO)
                self.__gameFrame.set_pixel_char(32, 20, back_carta)
                self.__gameFrame.set_pixel_color(32, 20, PRETO_CIANO)
                self.draw_frame()
                time.sleep(0.05)

                self.__gameFrame.set_pixel_char(32, 20, " ")
                self.__gameFrame.set_pixel_color(32, 20, PRETO_BRANCO)
                self.__gameFrame.set_pixel_char(31, 20, back_carta)
                self.__gameFrame.set_pixel_color(31, 20, PRETO_CIANO)
                self.draw_frame()
                time.sleep(0.05)
            
            elif i == 2:
                self.__gameFrame.set_pixel_char(32, 18, " ")
                self.__gameFrame.set_pixel_color(32, 18, PRETO_BRANCO)
                self.__gameFrame.set_pixel_char(31, 18, back_carta)
                self.__gameFrame.set_pixel_color(31, 18, PRETO_CIANO)
                self.draw_frame()
                time.sleep(0.05)


    def distribuir_cartas(self):
        deck = self.__trucoGame.get_baralho()
        queue = self.__trucoGame.get_fila_jogadores()
        for _ in range(4):
            player = queue.pop(0)
            deck_player = player.get_baralho()
            for _ in range(3):
                card = deck.topo()
                deck_player.add_carta(card.get_char(), card.get_valor())
            queue.append(player)

        
        self.entregar_carta_animation1()
        self.entregar_carta_animation2()
        self.entregar_carta_animation3()
        self.entregar_carta_animation4()
    
    
    def draw_cartas_jogador1(self):
        dupla1 = self.__trucoGame.get_dupla1()
        cards = dupla1.get_jogador1().get_baralho().get_cartas()
        for i in range(len(cards)):
            self.__gameFrame.set_pixel_char(48+i*2, 27, cards[i].get_char())
            self.__gameFrame.set_pixel_color(48+i*2, 27, PRETO_BRANCO)
        
        self.draw_frame()
            

    def descartar_carta_player1_animation(self, carta):
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


    def init_pares_cores(self):
        # Par 0 --> Texto branco, branckground preto 
        # Par 1 --> Texto ciano, background preto (verso das cartas)
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        # Par 2 --> Texto amarelo, background preto (borda da mesa)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        # Par 3 --> Texto vermelho, background preto (borda da mesa)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        # Par 4 --> Texto verde, background preto (Mensagem)
        curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
        # Par 5 --> Texto magenta, background preto (Mensagem)
        curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)        


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

    
    def draw_messages(self):
        self.clean_ledger_space()
        mensagens = self.__ledger.get_mensagens()
        for i in range(len(mensagens)):
            mensagem = mensagens[i].get_descricao()
            cor = mensagens[i].get_cor()
            for j in range(len(mensagem)):
                self.__gameFrame.set_pixel_char(102+j, 36-i, mensagem[j])
                self.__gameFrame.set_pixel_color(102+j, 36-i, cor)

        
        self.draw_frame()


    def clean_ledger_space(self):
        for y in range(1, 37):
            for x in range(102, 141):
                self.__gameFrame.set_pixel_char(x, y, " ")
                self.__gameFrame.set_pixel_color(x, y, PRETO_BRANCO)


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
        if char.isdigit():
            if 0 < int(char)-48 <= jogador.get_baraho().get_num_cartas():
                # Jogador descarta carta escolhida
                carta = jogador.descartar_carta(int(char)-48)
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
        
        else:
            if char == 't' and len(partida.get_rodada().partidas()) > 1:
                self.handle_truco_input()


    def handle_truco_input(self, jogador1, jogador2, partida):
        if jogador2 == self.__trucoGame.get_dupla1().get_jogador1():
            char = self.get_input_jogador()
        
        else:
            char = random.choice(['a', 'f', '6'])
        
        rodada = self.partida.get_rodada()    
        if char == 'a':
            rodada.set_estado(1)
            rodada.set_pontos(3)

        elif char == 'f':
            rodada.set_dupla_vencedora(jogador1.get_dupla())

        elif char == '6':
            rodada.set_estado(1)
            rodada.set_pontos(3)
            self.handle_6_input(jogador2, jogador1, partida)


    def handle_6_input(self, jogador1, jogador2, partida):
        pass

            