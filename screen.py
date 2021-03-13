import os

from headers import *


class Screen:

    def __init__(self, rows, columns):
        self.__rows = rows
        self.__columns = columns
        self.__move_down = False
        self.__level = 1
        self.__bricks = []
        self.__lives = 3
        self.__boss = None
        self.__paddle = None
        self.__score = 0
        self.__change_level = False
        self.grid = []

    def create_screen(self):
        self.grid = []
        for i in range(self.__rows):
            temp = []
            for j in range(self.__columns):
                temp.append(Back.BLACK + " " + Back.RESET)
            self.grid.append(temp)

    def move_down(self, val):
        self.__move_down = val

    def get_move_down(self):
        return self.__move_down

    def set_boss(self, val):
        self.__boss = val

    def get_boss(self):
        return self.__boss

    def set_paddle(self, val):
        self.__paddle = val

    def get_paddle(self):
        return self.__paddle

    def quit(self):
        os.system('tput reset')
        print("GAME OVER")
        print("SCORE : " + str(self.__score))
        if self.__level == 0:
            print("LEVEL : Boss level")
        else:
            print("LEVEL : " + str(self.__level))
        quit()

    def add_score(self, add):
        if add == 1:
            self.__score += 10
        elif add == 2:
            self.__score += 15
        elif add == 3:
            self.__score += 20
        elif add == 0:
            self.__score += 50
        # elif add == 4:

    def get_score(self):
        return self.__score

    def next_level(self):
        if 3 > self.__level > 0:
            self.__level += 1
        elif self.__level == 0:
            self.quit()
        else:
            self.__level = 0
        self.__move_down = False
        self.__change_level = False

    def change_level(self):
        self.__change_level = True

    def get_change_level(self):
        return self.__change_level

    def get_level(self):
        return self.__level

    def print_screen(self):
        for i in range(self.__rows):
            for j in range(self.__columns):
                print(self.grid[i][j], end='')

            print()


display = Screen(Screen_height, Screen_width)
