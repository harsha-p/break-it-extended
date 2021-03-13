from ball_powerup import *
from main_object import *


class Bullet(Object):
    def __init__(self, x, y, x_v=-1, boss=False):
        self.__x_v = x_v
        self.__y_v = 0
        self.__boss = boss
        self.__collided_brick_type = 0
        self.__collided_brick_x = 0
        self.__collided_brick_y = 0
        Object.__init__(self, x, y)

    def getbt(self):
        return self.__collided_brick_type, self.__collided_brick_x, self.__collided_brick_y

    def check_collision(self):
        if self.__boss:
            i = self.getx() + self.__x_v
            self.setx(i)
            j = self.gety()
            if i >= Screen_height - 1:
                return True
            if display.grid[i][j] == display.get_paddle().get_shape():
                display.get_paddle().dec_lives()
                return True
            self.display(BULLET)
            return
        else:
            i = self.getx() + self.__x_v
            self.setx(i)
            if self.__collided_brick_type != 0:
                return True
            j = self.gety()
            if i <= 0:
                return True
            val = 0
            try:
                val = brick_types.index(display.grid[i][j])
            except:
                val = 0
            if val > 0:
                if val == 1:
                    newpower = Powerup(i, j, self.__x_v, self.__y_v, random.randint(1, len(POWERUPS)))
                    new_powerups.append(newpower)
                display.add_score(val)
                self.__collided_brick_type = val
                self.__collided_brick_x = i
                self.__collided_brick_y = j
            self.display(BULLET)
