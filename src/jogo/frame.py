from pixel import Pixel


class Frame:
    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.__pixels = [[Pixel(x, y) for x in range(width)] for y in range(height)]
    

    def get_pixel(self, x, y):
        return self.__pixels[y][x]
    
    
    def set_pixel_char(self, x, y, char):
        self.__pixels[y][x].set_char(char)


    def set_pixel_color(self, x, y, color):
        self.__pixels[y][x].set_color(color)
    
    
    def get_width(self):
        return self.__width
    
    
    def get_height(self):
        return self.__height


    def set_pixels(self, pixels):
        self.__pixels = pixels

                