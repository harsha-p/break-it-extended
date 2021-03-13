from bullet import *


class Paddle(Object):
    def __init__(self, x, y, type):
        self.__type = type
        self.__lives = 3
        self.__on_hold = []
        self.__shape = Back.WHITE + " " + Back.RESET
        self.__paddle_hold = False
        self.__laser = False
        Object.__init__(self, x, y)

    def set_type(self, type):
        self.__type = type

    def show(self):
        self.display([[self.__shape] * paddle_sizes[self.__type]])

    def gettype(self):
        return self.__type

    def setshape(self, shape):
        self.__shape = shape

    def get_shape(self):
        return self.__shape

    def shoot(self):
        if not self.__laser:
            return
        b1 = Bullet(self.getx(), self.gety())
        b2 = Bullet(self.getx(), self.gety() + paddle_sizes[self.__type])
        bullets.append(b1)
        bullets.append(b2)

    def set_paddle_hold(self, paddle_hold):
        self.__paddle_hold = paddle_hold

    def get_paddle_hold(self):
        return self.__paddle_hold

    def set_laser(self, laser):
        self.__laser = laser

    def get_laser(self):
        return self.__laser

    def move_left(self):
        if self.gety() - paddle_step >= 0:
            self.sety(self.gety() - paddle_step)
            try:
                for ball in self.__on_hold:
                    ball.sety(ball.gety() - paddle_step)
            except:
                print(self.__on_hold)
                quit()
        else:
            for ball in self.__on_hold:
                if ball.gety() != 0:
                    ball.sety(ball.gety() - self.gety())
            self.sety(0)
        if display.get_level() == 0:
            display.get_boss().move(self.gety())

    def move_right(self):
        if self.gety() + paddle_sizes[self.__type] + paddle_step <= Screen_width:
            self.sety(self.gety() + paddle_step)
            for ball in self.__on_hold:
                ball.sety(ball.gety() + paddle_step)
        else:
            for ball in self.__on_hold:
                if self.gety() != (Screen_width - paddle_sizes[self.__type]):
                    ball.sety(ball.gety() + Screen_width - paddle_sizes[self.__type] - self.gety())
            self.sety(Screen_width - paddle_sizes[self.__type])
        if display.get_level() == 0:
            display.get_boss().move(self.gety())

    def release(self):
        self.__on_hold[0].set_hold(False)
        self.__on_hold.pop(0)

    def get_hold(self):
        return self.__on_hold

    def set_hold(self, ball):
        self.__on_hold.append(ball)
        ball.set_hold(True)

    def get_lives(self):
        return self.__lives

    def dec_lives(self):
        self.__lives -= 1
        while len(new_powerups):
            new_powerups.pop()
        for power in powerups:
            if power.getstatus() == 1:
                power.deactivate()
        if self.__lives == 0:
            display.quit()
