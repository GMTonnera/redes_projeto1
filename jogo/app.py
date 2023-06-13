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
            # Iniciar rodada
            self.__trucoGame.init_rodada()
            rodada = self.__trucoGame.get_rodada_atual()
            
            msg = InicioRodadaMensagem(len(self.__trucoGame.get_rodadas()))
            print(msg.get_descricao())
            self.enviarPacoteTodos(f"menssagem {msg.get_cor()} {msg.get_descricao()}")
            
            # Jogar as partidas da rodada
            while rodada.get_dupla_vencedora() is None:
                # Iniciar a partida
                rodada.init_partida()
                partida = rodada.get_partida_atual()
                
                # Desenhar as cartas do jogador1
                #self.draw_cartas_jogador1()
                
                # Adquirir as cartas que cada jogador descartou
                for i in range(4):
                    jogador = rodada.next_jogador()

                    #mega gambiarra 
                    
                    if jogador.get_dupla() == self.__trucoGame.get_dupla1():
                        rodada.set_pediu_truco(self.__trucoGame.get_dupla2())
                    else:
                        rodada.set_pediu_truco(self.__trucoGame.get_dupla1())

                    socketJogador = jogador.get_socket()
                    self.enviarPacote(f"seuturno 0", jogador.get_id())
                    c = int(socketJogador.recv(1024).decode("utf-8"))
                    
                    
                    #gambiarra suprema nao ta pronto essa bosta
                    if False:#c == ord('t'):
                        self.handle_input(c, jogador, partida)
                        self.enviarPacoteTodos(f"menssagem 5 {jogador.get_nome()} pediu truco")
                        self.enviarPacote(f"seuturno 1", proxjogador.get_id())
                        r = int(proxjogador.get_socket().recv(1024).decode("utf-8"))
                       
                        if r == ord('f'):
                            self.handle_input(c, proxjogador, partida)
                            break
                        elif (r == ord('t')):
                            self.enviarPacoteTodos(f"menssagem 5 {proxjogador.get_nome()} aumentou")
                            self.handle_input(c, proxjogador, partida)
                            c = int(socketJogador.recv(1024).decode("utf-8"))
                        elif (r == ord('a')):
                            self.enviarPacoteTodos(f"menssagem 5 {proxjogador.get_nome()} aceitou")
                            self.handle_input(c, proxjogador, partida)
                            c = int(socketJogador.recv(1024).decode("utf-8"))


                    if c == ord('f'):
                        self.handle_input(c, jogador, partida)
                        break
                    
                    
                    carta = self.handle_input(c, jogador, partida)
                    self.enviarPacoteTodos(f"desenharcarta {self.__trucoGame.get_rodada_atual().get_num_partidas()} {carta.get_char()} {jogador.get_offset()}")
                    
                else:
                    # Verificar vencedor da partida
                    partida.verificar_vencedor()
                    #self.final_partida()
                    
                    if partida.get_vencedor() is None:
                        msg = EmpatePartidaMensagem(len(rodada.get_partidas()))
                        self.enviarPacoteTodos(f"menssagem {msg.get_cor()} {msg.get_descricao()}")
                        print(msg.get_descricao())
                        self.enviarPacoteTodos("finalpartida -1")
                    
                    else:
                        msg = GanhadorPartidaMensagem(partida.get_vencedor(), len(rodada.get_partidas()))
                        self.enviarPacoteTodos(f"menssagem {msg.get_cor()} {msg.get_descricao()}")
                        print(msg.get_descricao())
                        self.enviarPacoteTodos(f"finalpartida {partida.get_vencedor().get_offset()}")


                    # Atualizar fila de jogadores
                    rodada.update_fila_jogadores() 

                # Verificar vencedor da rodada
                rodada.verificar_vencedor()
                if rodada.get_dupla_vencedora() is not None:
                    msg = GanhadorRodadaMenagem(rodada.get_dupla_vencedora().get_nome(), len(self.__trucoGame.get_rodadas()))
                    self.enviarPacoteTodos(f"menssagem {msg.get_cor()} {msg.get_descricao()}")         
                    print(msg.get_descricao())


            # Atualizar fila de jogadores para a próxima rodada
            self.__trucoGame.update_fila_jogadores()

            # Limpar baralho e inicializa-lo de novo
            self.__trucoGame.get_baralho().limpar()
            self.__trucoGame.init_baralho()
            self.__trucoGame.get_baralho().embaralhar()

            # Limpar o baralho dos jogadores
            self.__trucoGame.limpar_baralho_jogadores()
            
            self.enviarPacoteTodos("finalrodada 0")

            self.enviarPacoteTodos(f"placar {self.__trucoGame.get_dupla1().get_pontos()} {self.__trucoGame.get_dupla2().get_pontos()}")

            
            if (self.__trucoGame.get_dupla1().get_pontos() >= 12):
                print(f"Dupla vencedora: {self.__trucoGame.get_dupla1()}\n{self.__trucoGame.get_dupla2()}")
                self.enviarPacoteTodos("fim 0")
                return 
            
            elif (self.__trucoGame.get_dupla2().get_pontos() >= 12):
                print(f"Dupla vencedora: {self.__trucoGame.get_dupla2()}\n{self.__trucoGame.get_dupla1()}")
                self.enviarPacoteTodos("fim 1")
                return 



    def main(self):
        self.game()    

    

    def criar_jogo(self):
        # Criar instancia do jogo
        self.__trucoGame =  JogoTruco()
        
        # Criar duplas do jogo
        dupla1 = Dupla()
        dupla2 = Dupla()
        
        # Criar jogadores
        jogador1 = Jogador(0, self.__jogadores[0][0], dupla1, (50, 22), self.__jogadores[0][1], 0)
        jogador2 = Jogador(1, self.__jogadores[1][0], dupla1, (50, 14), self.__jogadores[1][1], 2)
        jogador3 = Jogador(2, self.__jogadores[2][0], dupla2, (58, 18), self.__jogadores[2][1], 1)
        jogador4 = Jogador(3, self.__jogadores[3][0], dupla2, (41, 18), self.__jogadores[3][1], 3)

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
        socket = self.__jogadores[jogador][1]
        socket.send(mensagem.encode("utf-8"))
        confirm = socket.recv(1024).decode("utf-8")
        if confirm == "confirmado":
            return
        else:
            print(confirm)
            print("erro não recebeu pacote")
            raise SystemExit

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
            self.enviarPacote(f"recebercarta {' '.join(cartasString)}", player.get_id())

            queue.append(player)



    def get_truco_game(self):
        return self.__trucoGame
      
        

    def get_input_jogador(self):
        return self.__window.getch()
    

    def handle_input(self, char, jogador, partida):
        if 49 <= char <= 51:
            if 0 < char-48 <= jogador.get_baralho().get_num_cartas():
                # Jogador descarta carta escolhida
                carta = jogador.descartar_carta(char-48)
                
                # Adicionar a carta na partida
                partida.add_carta(carta)

                # Criar mensagem de carta descartada
                msg = CartaJogadaMensagem(jogador, carta)
                self.enviarPacoteTodos(f"menssagem {msg.get_cor()} {msg.get_descricao()}")
                print(msg.get_descricao())

                #return True
                return carta
        
        # Pedir 
        #elif char == ord('t'):
        #    partida.get_rodada().set_estado(1, jogador)
            
        
        # Aceitar 
        elif char == ord('a'):
            partida.get_rodada().set_estado(2, jogador)
            
        # Fugir  
        elif char == ord('f'):
            partida.get_rodada().set_estado(4, jogador)
            estado =  partida.get_rodada().get_estado()
            
        # Aumentar/pedir truco
        elif char == ord('t'):
            partida.get_rodada().set_estado(3, jogador)
            

        return False
        



            