from bullet import *
from brick import *


class Ufo(Object):
    def __init__(self, y):
        self.__shape = [[ufo_shape] * paddle_sizes[1]]
        self.__lives = 10
        self.__count = 0
        Object.__init__(self, 4, y)

    def show(self):
        self.__count += 1
        if self.__count == 20:
            self.shoot()
            self.__count = 0
        self.display(self.__shape)

    def shoot(self):
        b1 = Bullet(self.getx(), self.gety() + len(self.__shape[-1]) // 2, 1, boss=True)
        bullets.append(b1)

    def move(self, y):
        self.sety(y)

    def spawn(self):
        x = self.__lives * 2
        y = 0
        while y + brick_length <= Screen_width:
            bricks.append(Brick(x, y, random.randint(1, 3)))
            y += brick_length

    def get_lives(self):
        return self.__lives

    def dec_lives(self):
        self.__lives -= 1
        if self.__lives == 4 or self.__lives == 7:
            self.spawn()
            pass
        if self.__lives == 0:
            display.quit()
