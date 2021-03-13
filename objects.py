import math
import random
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
                return
        if self.__rainbow:
            self.__count += 1
        if self.__count == 10 and self.__type != 0:
            self.__type = random.randint(1, 3)
            self.__count = 0

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
                return
        self.display(BRICKS[self.gettype()])


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
        self.__gravity += 0.1
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
