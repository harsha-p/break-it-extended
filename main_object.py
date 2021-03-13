from screen import *


class Object:

    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def getx(self):
        return self.__x

    def setx(self, x):
        self.__x = x

    def gety(self):
        return self.__y

    def sety(self, y):
        self.__y = y

    def display(self, shape):
        for i in range(self.__x, self.__x + len(shape)):
            for j in range(self.__y, self.__y + len(shape[0])):
                try:
                    display.grid[i][j] = shape[i - self.__x][j - self.__y]
                except:
                    print("ERR")
                    print(shape)
                    print(i, j, self.__x, self.__y)
                    quit()
