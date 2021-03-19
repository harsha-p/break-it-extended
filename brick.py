import random
from main_object import *


class Brick(Object):

    def __init__(self, x, y, brick_type):
        self.__type = brick_type
        self.__count = 0
        self.__rainbow = display.get_level() > 0 and random.randint(0, 10) < 1
        Object.__init__(self, x, y)

    def gettype(self):
        return self.__type

    def move_down(self):
        if display.get_move_down() and display.get_level() != 0:
            self.setx(self.getx() + 1)
        if self.getx() >= Screen_height - brick_height - 4:
            display.quit()

    def set_type(self, brick_type):
        self.__type = brick_type

    def check_collision(self):
        for laser in bullets:
            type, x, y = laser.getbt()
            if type == 0:
                continue
            if self.__type != type:
                continue
            if type == 4:
                continue
            bx = x - self.getx()
            by = y - self.gety()
            # if bx >= 0 and bx < brick_height and by >= 0 and by < brick_length:
            if 0 <= bx < brick_height and 0 <= by < brick_length:
                self.set_type(type - 1)
                self.__rainbow = False
                return

        for ball in BALLS:
            type, x, y = ball.getbt()
            if type == 0:
                continue
            if self.__type != type:
                continue
            if type == 4 and not ball.getthru():
                continue
            bx = x - self.getx()
            by = y - self.gety()
            # if bx >= 0 and bx < brick_height and by >= 0 and by < brick_length:
            if 0 <= bx < brick_height and 0 <= by < brick_length:
                if ball.getthru():
                    self.set_type(0)
                else:
                    self.set_type(type - 1)
                self.__rainbow = False
                return
        if self.__rainbow:
            self.__count += 1
        if self.__count == 5 and self.__type != 0:
            self.__type = random.randint(1, 3)
            self.__count = 0
        self.display(BRICKS[self.gettype()])
