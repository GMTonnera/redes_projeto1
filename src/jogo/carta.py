class Carta:
    def __init__(self, char, valor, baralho):
        self.__char = char
        self.__valor = valor
        self.__baralho = baralho

    
    def get_char(self):
        return self.__char
    

    def set_char(self, new_char):
        self.__char = new_char


    def get_valor(self):
        return self.__valor
    

    def set_valor(self, new_valor):
        self.__valor = new_valor


    def get_baralho(self):
        return self.__baralho
    

    def set_baralho(self, new_baralho):
        self.__baralho = new_baralho

    
    def __eq__(self, carta2):
        return (self.__valor == carta2.__valor)
    

    def __ne__(self, carta2):
        return (self.__valor != carta2.__valor)
    

    def __gt__(self, carta2):
        return (self.__valor > carta2.__valor)
    

    def __lt__(self, carta2):
        return (self.__valor < carta2.__valor)
    

    def __ge__(self, carta2):
        return (self.__valor >= carta2.__valor)
    

    def __le__(self, carta2):
        return (self.__valor <= carta2.__valor)
    
    
    def __repr__(self) -> str:
        return f'{self.__char}'