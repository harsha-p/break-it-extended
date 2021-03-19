import math
import random
from main_object import *


class Ball(Object):
    def __init__(self, x, y, x_velocity, y_velocity):
        self.__x_v = x_velocity
        self.__y_v = y_velocity
        self.__collided_brick_type = 0
        self.__collided_brick_x = 0
        self.__collided_brick_y = 0
        self.__on_hold = False
        self.__thru = False
        Object.__init__(self, x, y)

    def setxv(self, x_velocity):
        self.__x_v = x_velocity

    def getxv(self):
        return self.__x_v

    def setthru(self, thru):
        self.__thru = thru

    def getthru(self):
        return self.__thru

    def getbt(self):
        return self.__collided_brick_type, self.__collided_brick_x, self.__collided_brick_y

    def set_hold(self, value):
        self.__on_hold = value

    def get_hold(self):
        return self.__on_hold

    def setyv(self, y_velocity):
        self.__y_v = y_velocity

    def inc_speed(self):
        y = self.getyv()
        x = self.getxv()
        if y > 0:
            self.setyv(y + 2)
        else:
            self.setyv(y - 2)
        if x > 0:
            self.setxv(x + 2)
        else:
            self.setxv(x - 2)

    def dec_speed(self):
        y = self.getyv()
        x = self.getxv()
        if y > 0:
            self.setyv(y - 2)
        else:
            self.setyv(y + 2)
        if x > 0:
            self.setxv(x - 2)
        else:
            self.setxv(x + 2)

    def getyv(self):
        return self.__y_v

    def create_newball(self):
        paddle = display.get_paddle()
        yp = paddle.gety()
        yb = random.randint(yp, yp + paddle_sizes[paddle.gettype()])
        # ball = Ball(Screen_height-5, yb, -1, 1)
        ball = Ball(Screen_height - 5, yb, -1, 1)
        paddle.set_hold(ball)
        BALLS.append(ball)
        # BALLS.remove(self)
        return

    def check_collision(self):
        if self.__on_hold:
            self.display(BALL)
            return
        diry = 0
        jv = self.getyv()
        iv = self.getxv()
        i = self.getx()
        j = self.gety()
        if jv < 0:
            diry = -1
        else:
            diry = 1
        dirx = 0
        if iv < 0:
            dirx = -1
        else:
            dirx = 1
        paddle = display.get_paddle()
        # print(j,jv,diry,i,iv,dirx)
        for y in range(j, j + jv + diry, diry):
            for x in range(i, i + iv + dirx, dirx):
                # check border
                # print("XY",x,y)
                check = False
                if x < 0:
                    self.setxv(-self.getxv())
                    self.setx(0)
                    check = True
                elif x >= Screen_height - 1:
                    self.setx(Screen_height - 2)
                    self.setxv(-self.getxv())
                    BALLS.remove(self)
                    if len(BALLS) == 0:
                        paddle.dec_lives()
                        self.create_newball()
                    check = True
                if y < 0:
                    self.setyv(-self.getyv())
                    self.sety(0)
                    check = True
                elif y > Screen_width - 1:
                    self.setyv(-self.getyv())
                    self.sety(Screen_width - 1)
                    check = True
                if check:
                    self.display(BALL)
                    return
                # check brick
                val = 0
                try:
                    val = brick_types.index(display.grid[x][y])
                except:
                    val = 0
                if val > 0:
                    # found brick
                    # need to update collision strategy, should not check full rectangle !!!
                    # change to something using ratio
                    display.add_score(val)
                    self.__collided_brick_type = val
                    self.__collided_brick_x = x
                    self.__collided_brick_y = y
                    if (val == 1 or self.__thru) and display.get_level() != 0:
                        new_power = Powerup(x, y, self.getxv(), self.getyv(), random.randint(1, len(POWERUPS)))
                        new_powerups.append(new_power)
                    if self.__thru:
                        self.setx(self.getx() + self.getxv())
                        self.sety(self.gety() + self.getyv())
                        self.display(BALL)
                        return
                    posy = diry * (y - self.gety())
                    posx = dirx * (x - self.getx())
                    if posx == posy:
                        self.sety(y - diry)
                        self.setx(x - dirx)
                        self.setxv(-self.getxv())
                        self.setyv(-self.getyv())
                    elif posx > posy:
                        self.sety(y)
                        self.setx(x - dirx)
                        self.setxv(-self.getxv())
                    elif posx < posy:
                        self.setyv(-self.getyv())
                        self.sety(y - diry)
                        self.setx(x)
                    self.display(BALL)
                    return
                elif Screen_height > x > 0 and Screen_width > y > 0:
                    try:
                        if display.grid[x][y] == paddle.get_shape():
                            # move bricks down
                            for brick in bricks:
                                brick.move_down()
                            # add variey of speed in y
                            mid = paddle.gety() + int(paddle_sizes[paddle.gettype()] / 2)
                            self.sety(y)
                            self.setx(x - dirx)
                            self.setxv(-self.getxv())
                            self.setyv(self.getyv() + y - mid)
                            if paddle.get_paddle_hold():
                                paddle.set_hold(self)
                            self.display(BALL)
                            return
                    except:
                        pass
                    if display.grid[x][y] == ufo_shape:
                        display.add_score(0)
                        posy = diry * (y - self.gety())
                        posx = dirx * (x - self.getx())
                        if posx == posy:
                            self.sety(y - diry)
                            self.setx(x - dirx)
                            self.setxv(-self.getxv())
                            self.setyv(-self.getyv())
                        elif posx > posy:
                            self.sety(y)
                            self.setx(x - dirx)
                            self.setxv(-self.getxv())
                        elif posx < posy:
                            self.setyv(-self.getyv())
                            self.sety(y - diry)
                            self.setx(x)
                        self.display(BALL)
                        display.get_boss().dec_lives()
                        return
        self.setx(self.getx() + self.getxv())
        self.sety(self.gety() + self.getyv())
        self.display(BALL)


class Powerup(Object):
    def __init__(self, x, y, xv, yv, type, name="powerup"):
        self.__timer = 0
        self.__status = 0
        self.__gravity = xv
        self.__xv = 0
        self.__yv = yv
        self.name = name
        self.__type = type
        Object.__init__(self, x, y)

    def getstatus(self):
        return self.__status

    def gettype(self):
        return self.__type

    def setstatus(self, status):
        self.__status = status

    def addtimer(self):
        self.__timer += 100

    def setzero(self):
        self.__timer = 0

    def dectimer(self):
        self.__timer -= 1
        if self.__timer == 0:
            return True
        return False

    def gettimer(self):
        return self.__timer

    # def kill(self):
    #     powerups.remove(self)
    def deactivate(self):
        self.setstatus(0)

    def activate(self):
        type = self.gettype()
        # print("TYPE",type,self.getx(),self.gety())
        # print(printapowerups),type)
        pow = powerups[type - 1]
        if pow.getstatus() == 0:
            pow.setstatus(1)
        pow.addtimer()

    def check(self):
        x = self.getx()
        y = self.gety()
        self.__gravity += 0.2
        self.__xv = math.floor(self.__gravity)
        diry = 0
        jv = self.__yv
        iv = self.__xv
        i = x
        j = y
        if jv < 0:
            diry = -1
        else:
            diry = 1
        dirx = 0
        if iv < 0:
            dirx = -1
        else:
            dirx = 1
        paddle = display.get_paddle()
        # print(j,jv,diry,i,iv,dirx)
        for y in range(j, j + jv + diry, diry):
            for x in range(i, i + iv + dirx, dirx):
                # check border
                # print("XY",x,y)
                if display.grid[x][y] == paddle.get_shape():
                    self.activate()
                    return True
                if x < 0:
                    self.__gravity = - self.__gravity
                    self.__xv = math.floor(self.__gravity)
                    self.setx(0)
                    return False
                elif x >= Screen_height - 1:
                    self.setx(Screen_height - 2)
                    self.__xv = - self.__xv
                    return True
                if y < 0:
                    self.__yv = - self.__yv
                    self.sety(0)
                    return False
                elif y > Screen_width - 2:
                    self.__yv = - self.__yv
                    self.sety(Screen_width - 2)
                    return False
        # self.__xv = self.__gravity // 1
        self.setx(self.getx() + self.__xv)
        self.sety(self.gety() + self.__yv)
        self.display(POWERUPS[self.gettype() - 1])
        return False


class expandpaddle(Powerup):

    def __init__(self):
        Powerup.__init__(self, 0, 0, 0, 0, 0, "EXP")

    def deactivate(self):
        self.setstatus(0)
        self.setzero()
        display.get_paddle().set_type(1)

    def activate(self):
        paddle = display.get_paddle()
        # not working (paddle at right border)
        if self.getstatus() == 1:
            sz = paddle.gety() + paddle_sizes[2]
            if sz >= Screen_width:
                paddle.sety(paddle.gety() + sz - Screen_width)
            paddle.set_type(2)
            if self.dectimer():
                self.deactivate()


class ShrinkPaddle(Powerup):

    def __init__(self):
        Powerup.__init__(self, 0, 0, 0, 0, 1, "SHR")

    def deactivate(self):
        self.setstatus(0)
        self.setzero()
        display.get_paddle().set_type(1)

    def activate(self):
        if self.getstatus() == 1:
            display.get_paddle().set_type(0)
            if self.dectimer():
                self.deactivate()


class DoubleTrouble(Powerup):

    def __init__(self):
        Powerup.__init__(self, 0, 0, 0, 0, 2, "DTR")

    def deactivate(self):
        # print("LOLOL")
        self.setstatus(0)
        # print(len(BALLS),"BALLS")
        if len(BALLS) == 2:
            BALLS.pop(1)
        self.setzero()

    def activate(self):
        # print("status",self.getstatus())
        if self.getstatus() == 1:
            if len(BALLS) == 1:
                # pass
                # add ball
                b = BALLS[0]
                if b.getx() < Screen_height - 2:
                    BALLS.append(Ball(b.getx(), b.gety(), b.getxv(), -b.getyv()))
                else:
                    self.deactivate()
            if self.dectimer():
                self.deactivate()
            # print("TIMER",self.gettimer())
        else:
            self.deactivate()


class FastBall(Powerup):

    def __init__(self):
        self.lol = 0
        Powerup.__init__(self, 0, 0, 0, 0, 3, "FSB")

    def deactivate(self):
        # pass
        self.setstatus(0)
        self.lol = 0
        for ball in BALLS:
            ball.dec_speed()
        self.setzero()

    def activate(self):
        if self.getstatus() == 1:
            if self.lol == 0:
                self.lol = 1
                for ball in BALLS:
                    ball.inc_speed()
            if self.dectimer():
                self.deactivate()
            # print("TIMER", self.gettimer())
        # else:
        #     self.deactivate()


class ThruBall(Powerup):

    def __init__(self):
        Powerup.__init__(self, 0, 0, 0, 0, 4, "THB")

    def deactivate(self):
        self.setstatus(0)
        for ball in BALLS:
            ball.setthru(False)
        self.setzero()

    def activate(self):
        if self.getstatus() == 1:
            # code
            for ball in BALLS:
                ball.setthru(True)
            if self.dectimer():
                self.deactivate()
        else:
            self.deactivate()


class PaddleGrab(Powerup):

    def __init__(self):
        Powerup.__init__(self, 0, 0, 0, 0, 5, "GRB")

    def deactivate(self):
        self.setstatus(0)
        display.get_paddle().set_paddle_hold(False)
        self.setzero()

    def activate(self):
        if self.getstatus() == 1:
            display.get_paddle().set_paddle_hold(True)
            if self.dectimer():
                self.deactivate()
        else:
            self.deactivate()


class ShootPaddle(Powerup):

    def __init__(self):
        Powerup.__init__(self, 0, 0, 0, 0, 6, "SHB")

    def deactivate(self):
        self.setstatus(0)
        display.get_paddle().set_laser(False)
        display.get_paddle().setshape(Back.WHITE + " " + Back.RESET)
        # paddle.setlaser(False)
        self.setzero()

    def activate(self):
        if self.getstatus() == 1:
            paddle = display.get_paddle()
            paddle.setshape(Back.RED + "|" + Back.RESET)
            paddle.set_laser(True)
            if self.dectimer():
                self.deactivate()
        else:
            self.deactivate()
