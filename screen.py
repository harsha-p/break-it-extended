import os

from headers import *


class Screen:

    def __init__(self, rows, columns):
        self.__rows = rows
        self.__columns = columns
        self.__movedown = False
        self.__level = 1
        self.__lives = 3
        self.__score = 0
        self.__change_level = False
        self.grid = []

    def create_screen(self):
        self.grid = []
        for i in range(self.__rows):
            self.temp = []
            for j in range(self.__columns):
                self.temp.append(Back.BLACK + " " + Back.RESET)
            self.grid.append(self.temp)

    def move_down(self, val):
        self.__movedown = val

    def get_move_down(self):
        return self.__movedown

    def getlives(self):
        return self.__lives

    def declives(self):
        self.__lives -= 1
        if self.__lives == 0:
            # pass
            self.quit()

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
        # elif add == 4:

    def get_score(self):
        return self.__score

    def next_level(self):
        if self.__level < 3 and self.__level > 0:
            self.__level += 1
        elif self.__level == 0:
            self.quit()
        else:
            self.__level = 0
        self.__movedown = False
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
                # print(Back.BLACK + self.grid[i][j] + Back.RESET, end='')
                print(self.grid[i][j], end='')

            print()


display = Screen(Screen_height, Screen_width)
