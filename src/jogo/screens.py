from constants import FRAME_WIDTH, FRAME_HEIGHT, PRETO_CIANO
from pixel import Pixel
from unicode_chars import *


def make_menuScreen():
    menu = [[Pixel(x, y) for x in range(FRAME_WIDTH)] for y in range(FRAME_HEIGHT)]
    # Fazer o T (x + 3) (y + 5)
    menu[10][43].set_char(box_simples_ponta_es)
    menu[11][43].set_char(box_simples_ponta_ei) 
    menu[10][53].set_char(box_simples_ponta_ds) 
    menu[11][53].set_char(box_simples_ponta_di)  
    menu[11][47].set_char(box_simples_ponta_ds)  
    menu[11][49].set_char(box_simples_ponta_es)  
    menu[10][44].set_char(box_simples_horinzontal)  
    menu[10][45].set_char(box_simples_horinzontal)  
    menu[10][46].set_char(box_simples_horinzontal)  
    menu[10][47].set_char(box_simples_horinzontal)  
    menu[10][48].set_char(box_simples_horinzontal)  
    menu[10][49].set_char(box_simples_horinzontal)  
    menu[10][50].set_char(box_simples_horinzontal)  
    menu[10][51].set_char(box_simples_horinzontal)  
    menu[10][52].set_char(box_simples_horinzontal)  
    menu[11][44].set_char(box_simples_horinzontal)  
    menu[11][45].set_char(box_simples_horinzontal)  
    menu[11][46].set_char(box_simples_horinzontal)  
    menu[11][50].set_char(box_simples_horinzontal)  
    menu[11][51].set_char(box_simples_horinzontal)  
    menu[11][52].set_char(box_simples_horinzontal)  
    menu[12][47].set_char(box_simples_vertical)  
    menu[12][49].set_char(box_simples_vertical)  
    menu[13][47].set_char(box_simples_vertical)  
    menu[13][49].set_char(box_simples_vertical)  
    menu[14][47].set_char(box_simples_vertical)  
    menu[14][49].set_char(box_simples_vertical)  
    menu[15][47].set_char(box_simples_ponta_ei)  
    menu[15][49].set_char(box_simples_ponta_di)  
    menu[15][48].set_char(box_simples_horinzontal)          
    
    # Fazer o R
    menu[10][54].set_char(box_simples_ponta_es)  
    menu[10][60].set_char(box_simples_ponta_ds)  
    menu[13][60].set_char(box_simples_ponta_di)  
    menu[13][56].set_char(box_simples_ponta_es)  
    menu[15][54].set_char(box_simples_ponta_ei)  
    menu[15][56].set_char(box_simples_ponta_di)  
    menu[11][56].set_char(box_simples_ponta_es)  
    menu[11][58].set_char(box_simples_ponta_ds)  
    menu[12][56].set_char(box_simples_ponta_ei)  
    menu[12][58].set_char(box_simples_ponta_di)  
    menu[14][57].set_char(box_simples_ponta_ei)  
    menu[14][58].set_char(box_simples_ponta_ds)  
    menu[13][57].set_char(box_simples_ponta_ds)  
    menu[13][59].set_char(box_simples_ponta_es)  
    menu[14][58].set_char(box_simples_ponta_ds)  
    menu[15][60].set_char(box_simples_ponta_di)  
    menu[15][59].set_char(box_simples_horinzontal)  
    menu[15][58].set_char(box_simples_ponta_ei)  
    menu[14][60].set_char(box_simples_ponta_ds)  
    menu[14][59].set_char(box_simples_ponta_ei)  
    menu[10][55].set_char(box_simples_horinzontal)  
    menu[10][56].set_char(box_simples_horinzontal)  
    menu[10][57].set_char(box_simples_horinzontal)  
    menu[10][58].set_char(box_simples_horinzontal)  
    menu[10][59].set_char(box_simples_horinzontal)  
    menu[10][55].set_char(box_simples_horinzontal)  
    menu[11][57].set_char(box_simples_horinzontal)  
    menu[12][57].set_char(box_simples_horinzontal)  
    menu[15][55].set_char(box_simples_horinzontal)  
    menu[11][54].set_char(box_simples_vertical)  
    menu[12][54].set_char(box_simples_vertical)  
    menu[13][54].set_char(box_simples_vertical)  
    menu[14][54].set_char(box_simples_vertical)  
    menu[14][56].set_char(box_simples_vertical)  
    menu[11][60].set_char(box_simples_vertical)  
    menu[12][60].set_char(box_simples_vertical)  

    # Fazer o U
    menu[10][61].set_char(box_simples_ponta_es)  
    menu[10][63].set_char(box_simples_ponta_ds)  
    menu[10][66].set_char(box_simples_ponta_es)  
    menu[10][68].set_char(box_simples_ponta_ds)  
    menu[15][61].set_char(box_simples_ponta_ei)  
    menu[15][68].set_char(box_simples_ponta_di)  
    menu[14][63].set_char(box_simples_ponta_ei)  
    menu[14][66].set_char(box_simples_ponta_di)  
    menu[11][61].set_char(box_simples_vertical)  
    menu[12][61].set_char(box_simples_vertical)  
    menu[13][61].set_char(box_simples_vertical)  
    menu[14][61].set_char(box_simples_vertical)  
    menu[11][63].set_char(box_simples_vertical)  
    menu[12][63].set_char(box_simples_vertical)  
    menu[13][63].set_char(box_simples_vertical)  
    menu[11][66].set_char(box_simples_vertical)  
    menu[12][66].set_char(box_simples_vertical)  
    menu[13][66].set_char(box_simples_vertical)  
    menu[11][68].set_char(box_simples_vertical)  
    menu[12][68].set_char(box_simples_vertical)  
    menu[13][68].set_char(box_simples_vertical)  
    menu[14][68].set_char(box_simples_vertical)  
    menu[10][62].set_char(box_simples_horinzontal)  
    menu[10][67].set_char(box_simples_horinzontal)  
    menu[14][64].set_char(box_simples_horinzontal)  
    menu[14][65].set_char(box_simples_horinzontal)  
    menu[15][62].set_char(box_simples_horinzontal)  
    menu[15][63].set_char(box_simples_horinzontal)  
    menu[15][64].set_char(box_simples_horinzontal)  
    menu[15][65].set_char(box_simples_horinzontal)  
    menu[15][66].set_char(box_simples_horinzontal)  
    menu[15][67].set_char(box_simples_horinzontal)  

    # Fazer o C
    menu[10][69].set_char(box_simples_ponta_es)  
    menu[10][76].set_char(box_simples_ponta_ds)  
    menu[11][71].set_char(box_simples_ponta_es)  
    menu[11][76].set_char(box_simples_ponta_di)  
    menu[14][71].set_char(box_simples_ponta_ei)  
    menu[14][76].set_char(box_simples_ponta_ds)  
    menu[15][69].set_char(box_simples_ponta_ei)  
    menu[15][76].set_char(box_simples_ponta_di)  
    menu[10][70].set_char(box_simples_horinzontal)  
    menu[10][71].set_char(box_simples_horinzontal)  
    menu[10][72].set_char(box_simples_horinzontal)  
    menu[10][73].set_char(box_simples_horinzontal)  
    menu[10][74].set_char(box_simples_horinzontal)  
    menu[10][75].set_char(box_simples_horinzontal)  
    menu[11][72].set_char(box_simples_horinzontal)  
    menu[11][73].set_char(box_simples_horinzontal)  
    menu[11][74].set_char(box_simples_horinzontal)  
    menu[11][75].set_char(box_simples_horinzontal)  
    menu[14][72].set_char(box_simples_horinzontal)  
    menu[14][73].set_char(box_simples_horinzontal)  
    menu[14][74].set_char(box_simples_horinzontal)  
    menu[14][75].set_char(box_simples_horinzontal)  
    menu[15][70].set_char(box_simples_horinzontal)  
    menu[15][71].set_char(box_simples_horinzontal)  
    menu[15][72].set_char(box_simples_horinzontal)  
    menu[15][73].set_char(box_simples_horinzontal)  
    menu[15][74].set_char(box_simples_horinzontal)  
    menu[15][75].set_char(box_simples_horinzontal)  
    menu[11][69].set_char(box_simples_vertical)  
    menu[12][69].set_char(box_simples_vertical)  
    menu[13][69].set_char(box_simples_vertical)  
    menu[14][69].set_char(box_simples_vertical)  
    menu[12][71].set_char(box_simples_vertical)  
    menu[13][71].set_char(box_simples_vertical)  
    
    # Fazer o O
    menu[10][77].set_char(box_simples_ponta_es)  
    menu[10][84].set_char(box_simples_ponta_ds)  
    menu[15][77].set_char(box_simples_ponta_ei)  
    menu[15][84].set_char(box_simples_ponta_di)  
    menu[11][79].set_char(box_simples_ponta_es)  
    menu[11][82].set_char(box_simples_ponta_ds)  
    menu[14][79].set_char(box_simples_ponta_ei)  
    menu[14][82].set_char(box_simples_ponta_di)  
    menu[10][78].set_char(box_simples_horinzontal)  
    menu[10][79].set_char(box_simples_horinzontal)  
    menu[10][80].set_char(box_simples_horinzontal)  
    menu[10][81].set_char(box_simples_horinzontal)  
    menu[10][82].set_char(box_simples_horinzontal)  
    menu[10][83].set_char(box_simples_horinzontal)  
    menu[11][80].set_char(box_simples_horinzontal)  
    menu[11][81].set_char(box_simples_horinzontal)  
    menu[14][80].set_char(box_simples_horinzontal)  
    menu[14][81].set_char(box_simples_horinzontal)  
    menu[15][78].set_char(box_simples_horinzontal)  
    menu[15][79].set_char(box_simples_horinzontal)  
    menu[15][80].set_char(box_simples_horinzontal)  
    menu[15][81].set_char(box_simples_horinzontal)  
    menu[15][82].set_char(box_simples_horinzontal)  
    menu[15][83].set_char(box_simples_horinzontal)  
    menu[11][77].set_char(box_simples_vertical)  
    menu[12][77].set_char(box_simples_vertical)  
    menu[13][77].set_char(box_simples_vertical)  
    menu[14][77].set_char(box_simples_vertical)  
    menu[12][79].set_char(box_simples_vertical)  
    menu[13][79].set_char(box_simples_vertical)  
    menu[12][82].set_char(box_simples_vertical)  
    menu[13][82].set_char(box_simples_vertical)  
    menu[11][84].set_char(box_simples_vertical)  
    menu[12][84].set_char(box_simples_vertical)  
    menu[13][84].set_char(box_simples_vertical)  
    menu[14][84].set_char(box_simples_vertical)  
    
    # Escrever Jogar
    menu[20][63].set_char('J') 
    menu[20][64].set_char('o') 
    menu[20][65].set_char('g') 
    menu[20][66].set_char('a') 
    menu[20][67].set_char('r') 

    # Desenhar a seta na posicao inicial
    menu[20][61].set_char('>')

    return menu


def make_gameScreen():
    gameScreen = [[Pixel(x, y) for x in range(FRAME_WIDTH)] for y in range(FRAME_HEIGHT)]
    
    # Fazer a borda
    gameScreen[0][0].set_char(box_dupla_ponta_es) 
    gameScreen[0][FRAME_WIDTH-1].set_char(box_dupla_ponta_ds)  
    gameScreen[FRAME_HEIGHT-1][0].set_char(box_dupla_ponta_ei)  
    gameScreen[FRAME_HEIGHT-1][FRAME_WIDTH-1].set_char(box_dupla_ponta_di)  
    gameScreen[0][100].set_char(box_dupla_horinzontal_baixo)  
    gameScreen[FRAME_HEIGHT-1][100].set_char(box_dupla_horizontal_cima)  
    
    for i in range(1, FRAME_WIDTH-1):
        if i != 100:
            gameScreen[0][i].set_char(box_dupla_horizontal)
            gameScreen[FRAME_HEIGHT-1][i].set_char(box_dupla_horizontal)
    
    for i in range(1, FRAME_HEIGHT-1):
        gameScreen[i][0].set_char(box_dupla_vertical)  
        gameScreen[i][100].set_char(box_dupla_vertical)  
        gameScreen[i][FRAME_WIDTH-1].set_char(box_dupla_vertical)  
    

    # Fazer a mesa
    gameScreen[9][30].set_char(box_simples_ponta_es)  
    
    gameScreen[9][69].set_char(box_simples_ponta_ds)  
    
    gameScreen[28][30].set_char(box_simples_ponta_ei)  
    
    gameScreen[28][69].set_char(box_simples_ponta_di)  
    
    for i in range(10, 28):
        gameScreen[i][30].set_char(box_simples_vertical)  
        gameScreen[i][69].set_char(box_simples_vertical)  
        
    for i in range(31, 69):
        gameScreen[9][i].set_char(box_simples_horinzontal)
        gameScreen[28][i].set_char(box_simples_horinzontal)
        

    # Colocar o baralho no centro
    gameScreen[18][50].set_char(back_carta)
    gameScreen[18][50].set_color(PRETO_CIANO)

    return gameScreen


def make_queueScreen():
    q_screen = [[Pixel(x, y) for x in range(FRAME_WIDTH)] for y in range(FRAME_HEIGHT)]
    # Escrever "Aguardando outros jogadores..."
    q_screen[15][55].set_char('A') 
    q_screen[15][56].set_char('g') 
    q_screen[15][57].set_char('u') 
    q_screen[15][58].set_char('a') 
    q_screen[15][59].set_char('r') 
    q_screen[15][60].set_char('d') 
    q_screen[15][61].set_char('a') 
    q_screen[15][62].set_char('n') 
    q_screen[15][63].set_char('d') 
    q_screen[15][64].set_char('o') 
    q_screen[15][65].set_char(' ') 
    q_screen[15][66].set_char('o') 
    q_screen[15][67].set_char('u') 
    q_screen[15][68].set_char('t') 
    q_screen[15][69].set_char('r') 
    q_screen[15][70].set_char('o') 
    q_screen[15][71].set_char('s') 
    q_screen[15][72].set_char(' ') 
    q_screen[15][73].set_char('j') 
    q_screen[15][74].set_char('o') 
    q_screen[15][75].set_char('g') 
    q_screen[15][76].set_char('a') 
    q_screen[15][77].set_char('d') 
    q_screen[15][78].set_char('o') 
    q_screen[15][79].set_char('r') 
    q_screen[15][80].set_char('e') 
    q_screen[15][81].set_char('s') 
    q_screen[15][82].set_char('.') 
    q_screen[15][83].set_char('.') 
    q_screen[15][84].set_char('.') 

    return q_screen



MENU_SCREEN = make_menuScreen()

GAME_SCREEN = make_gameScreen()

QUEUE_SCREEN = make_queueScreen()