from constants import PRETO_BRANCO

class Pixel:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.__char = None
        self.__color = PRETO_BRANCO


    def get_x(self):
        return self.__x
    

    def set_x(self, x):
        self.__x = x

    
    def get_y(self):
        return self.__y
    

    def set_y(self, y):
        self.__y = y

    
    def get_char(self):
        return self.__char
    

    def set_char(self, char):
        self.__char = char


    def get_color(self):
        return self.__color
    

    def set_color(self, color):
        self.__color = color