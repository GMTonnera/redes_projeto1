from frame import Frame
from constants import *
import curses
from screens import MENU_SCREEN, GAME_SCREEN, make_queueScreen
from frame import Frame
from unicode_chars import *
from log_mensagens import LedgerMessages
import time
import socket
from threading import Thread


class JogoCliente:
    def __init__(self, a, n):
        # Janela
        self.__window = curses.initscr()
        
        # Frame do jogo
        self.__gameFrame = Frame(FRAME_WIDTH, FRAME_HEIGHT)
        
        # Frame do menu
        self.__menuFrame = Frame(FRAME_WIDTH, FRAME_HEIGHT)
        
        # Frame da fila
        self.__queueFrame = Frame(FRAME_WIDTH, FRAME_HEIGHT)

        # Ledger de Mensagens
        self.__ledger = LedgerMessages(36)

        self.__state = 0

        # Inicializar o frame da fila
        #self.__queueFrame.set_pixels(QUEUE_SCREEN)

        # Inilizar o frame de menu
        self.__menuFrame.set_pixels(MENU_SCREEN)

        # Inicializar o frame do jogo
        self.__gameFrame.set_pixels(GAME_SCREEN)

        #socket
        self.__socket = None

        #endereço
        self.__address = a

        self.__cards = None

        self.__nome = n

        self.__jogador = None

        self.__dupla1 = None
        self.__dupla2 = None
        self.__placar = (0, 0)

        #fila de "requisições"
        self.__thread = None
        self.__fila = []

    
    def threadEscuta(self):
        while True:
            tipo, data = self.__socket.recv(1024).decode("utf-8").split(maxsplit=1)
            self.__fila.append((tipo, data))
            self.__socket.sendall("confirmado".encode("utf-8"))




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
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.__socket.connect(self.__address)
            self.__socket.sendall(self.__nome.encode("utf-8"))
        except:
            print("falha na conexão")
            raise SystemExit
       
        while True:   
            tipo, data = self.__socket.recv(1024).decode("utf-8").split(maxsplit=1)
            if tipo == "start":
                num, nomes = data.split(maxsplit=1)
                nomes = nomes.split()
                
                if (num == "0") or (num == "3"):
                    self.__jogador = int(num)
                elif (num == "1"):
                    self.__jogador = 2
                elif (num == "2"):
                    self.__jogador = 1


                self.__dupla1 = f"{nomes[0]} e {nomes[1]}"
                self.__dupla2 = f"{nomes[2]} e {nomes[3]}"
                self.__state = 2
                self.__socket.sendall("start".encode("utf-8"))
                break
            elif tipo == "fila":
                self.__queueFrame.set_pixels(make_queueScreen(data))
                self.__window.clear()
                self.draw_frame()


                
    def game(self):
        self.__thread = Thread(target=self.threadEscuta, daemon=True)
        self.__thread.start()
        
        
        while True:
            self.__window.clear()
            self.draw_frame()
            self.draw_placar()
            if len(self.__fila) > 0:
                tipo, data = self.__fila.pop(0)
                if tipo == "recebercarta":
                    self.__cards = data.split()
                    self.entregar_carta_animation1()
                    self.entregar_carta_animation2()
                    self.entregar_carta_animation3()
                    self.entregar_carta_animation4()                        
                    self.__window.clear()
                    self.draw_frame()


                elif tipo == "seuturno":
                    self.__ledger.add_mensagem((5, "Sua vez!"))
                    self.draw_messages()
                    c = str(self.get_input_jogador())
                    self.__socket.sendall(c.encode("utf-8"))


                elif tipo == "menssagem":
                    msg = tuple(data.split(maxsplit=1))
                    self.__ledger.add_mensagem(msg)
                    self.draw_messages()


                # 0 2 1 3
                elif tipo == "desenharcarta":
                    numPartidas, carta, jogador = data.split()
                    offset = int(jogador) - self.__jogador
                    if offset == 0:
                        self.descartar_carta_player1_animation(carta, numPartidas)
                    elif (offset == 1) or (offset == -3):
                        self.descartar_carta_player2_animation(carta, numPartidas)
                    elif (offset == 2) or (offset == -2):
                        self.descartar_carta_player3_animation(carta, numPartidas)
                    elif (offset == 3) or (offset == -1):
                        self.descartar_carta_player4_animation(carta, numPartidas)


                elif tipo == "placar": 
                    self.__placar = tuple(data.split().map(int))

                elif tipo == "finalpartida":
                    self.final_partida_animation()


                elif tipo == "finalrodada":
                    self.final_rodada_animation()
                    self.__cards.clear()


                elif tipo == "teste":
                    curses.echo()
                    curses.nocbreak()
                    curses.endwin()    
                    
                    raise SystemExit

            
            


    def main(self):
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
                        self.__window.addch(y, x, ord(self.__menuFrame.get_pixel(x, y).get_char()), curses.color_pair(self.__menuFrame.get_pixel(x, y).get_color()))

                    elif self.__state == 1:
                        self.__window.addch(y, x, ord(self.__queueFrame.get_pixel(x, y).get_char()), curses.color_pair(self.__queueFrame.get_pixel(x, y).get_color()))
                        
                    elif self.__state == 2:
                        self.__window.addch(y, x, ord(self.__gameFrame.get_pixel(x, y).get_char()), curses.color_pair(self.__gameFrame.get_pixel(x, y).get_color()))
                    
                except:
                    pass

        self.__window.refresh()



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



    def draw_cartas_jogador1(self):
        for i in range(len(self.__cards)):
            self.__gameFrame.set_pixel_char(48+i*2, 27, self.__cards[i])
            self.__gameFrame.set_pixel_color(48+i*2, 27, PRETO_BRANCO)
        
        self.draw_frame()

    def draw_cartas_jogador2(self):
        for i in range(len(self.__cards)):
            self.__gameFrame.set_pixel_char(48+i*2, 27, self.__cards[i])
            self.__gameFrame.set_pixel_color(48+i*2, 27, PRETO_BRANCO)
        
        self.draw_frame()

    def draw_cartas_jogador3(self):
        for i in range(len(self.__cards)):
            self.__gameFrame.set_pixel_char(48+i*2, 27, self.__cards[i])
            self.__gameFrame.set_pixel_color(48+i*2, 27, PRETO_BRANCO)
        
        self.draw_frame()

    def draw_cartas_jogador4(self):
        for i in range(len(self.__cards)):
            self.__gameFrame.set_pixel_char(48+i*2, 27, self.__cards[i])
            self.__gameFrame.set_pixel_color(48+i*2, 27, PRETO_BRANCO)
        
        self.draw_frame()


    def get_input_jogador(self):
        return self.__window.getch()


    def draw_placar(self):
        dupla1_str = f"{self.__dupla1}: {self.__placar[0]}"
        dupla2_str = f"{self.__dupla2}: {self.__placar[1]}"

        for i in range(len(dupla1_str)):
            self.__gameFrame.set_pixel_char(i+1, 35, dupla1_str[i])
        
        for i in range(len(dupla2_str)):
            self.__gameFrame.set_pixel_char(i+1, 36, dupla2_str[i])

        #self.draw_frame()


    def draw_messages(self):
        self.clean_ledger_space()
        mensagens = self.__ledger.get_mensagens()
        for i in range(len(mensagens)):
            mensagem = mensagens[i][1]
            cor = int(mensagens[i][0])
            for j in range(len(mensagem)):
                self.__gameFrame.set_pixel_char(102+j, 36-i, mensagem[j])
                self.__gameFrame.set_pixel_color(102+j, 36-i, cor)

        
        self.draw_frame()


    def clean_ledger_space(self):
        for y in range(1, 37):
            for x in range(102, 141):
                self.__gameFrame.set_pixel_char(x, y, " ")
                self.__gameFrame.set_pixel_color(x, y, PRETO_BRANCO)



    def descartar_carta_player1_animation(self, carta, num_partidas):
        self.__gameFrame.set_pixel_char(50, 22, carta)
        self.draw_cartas_jogador1()
        if num_partidas == 1:
            self.__gameFrame.set_pixel_char(52, 27, " ")
            self.__gameFrame.set_pixel_color(52, 27, PRETO_BRANCO)

        elif num_partidas == 2:
            self.__gameFrame.set_pixel_char(50, 27, " ")
            self.__gameFrame.set_pixel_color(50, 27, PRETO_BRANCO)

        else:
            self.__gameFrame.set_pixel_char(48, 27, " ")
            self.__gameFrame.set_pixel_color(48, 27, PRETO_BRANCO)
        
        self.draw_frame()


    def descartar_carta_player2_animation(self, carta, num_partidas):
        self.__gameFrame.set_pixel_char(58, 18, carta)
        if num_partidas == 1:
            self.__gameFrame.set_pixel_char(67, 20, " ")
            self.__gameFrame.set_pixel_color(67, 20, PRETO_BRANCO)

        elif num_partidas == 2:
            self.__gameFrame.set_pixel_char(67, 18, " ")
            self.__gameFrame.set_pixel_color(67, 18, PRETO_BRANCO)

        else:
            self.__gameFrame.set_pixel_char(67, 16, " ")
            self.__gameFrame.set_pixel_color(67, 16, PRETO_BRANCO)

        self.draw_frame()


    def descartar_carta_player3_animation(self, carta, num_partidas):
        self.__gameFrame.set_pixel_char(50, 14, carta)
        if num_partidas == 1:
            self.__gameFrame.set_pixel_char(52, 10, " ")
            self.__gameFrame.set_pixel_color(52, 10, PRETO_BRANCO)

        elif num_partidas == 2:
            self.__gameFrame.set_pixel_char(50, 10, " ")
            self.__gameFrame.set_pixel_color(50, 10, PRETO_BRANCO)

        else:
            self.__gameFrame.set_pixel_char(48, 10, " ")
            self.__gameFrame.set_pixel_color(48, 10, PRETO_BRANCO)

        self.draw_frame()


    def descartar_carta_player4_animation(self, carta, num_partidas):
        self.__gameFrame.set_pixel_char(41, 18, carta)
        if num_partidas == 1:
            self.__gameFrame.set_pixel_char(31, 16, " ")
            self.__gameFrame.set_pixel_color(31, 16, PRETO_BRANCO)

        elif num_partidas == 2:
            self.__gameFrame.set_pixel_char(31, 18, " ")
            self.__gameFrame.set_pixel_color(31, 18, PRETO_BRANCO)

        else:
            self.__gameFrame.set_pixel_char(31, 20, " ")
            self.__gameFrame.set_pixel_color(31, 20, PRETO_BRANCO)

        self.draw_frame()


    def final_partida_animation(self):      
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
