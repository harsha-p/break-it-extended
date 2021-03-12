from objects import *
from input import *
from headers import *


def checkpowerups():
    i = 0
    while i < len(newpowerups):
        if newpowerups[i].check(paddle):
            newpowerups.pop(i)
        else:
            i += 1


def setnewlevel():
    x = 4
    bricks.clear()
    BALLS.clear()
    powerups.clear()
    newpowerups.clear()
    if display.get_level() <= 3:
        while x < Screen_height - 16:
            y = 6
            temp = []
            while y + brick_length <= Screen_width - 6:
                if random.randint(1, 100) <= display.get_level() * 20:
                    if random.randint(1, 10) <= 9:
                        bricks.append(Brick(x, y, random.randint(1, 3)))
                        # bricks.append(Brick(x, y, 1))
                    else:
                        bricks.append(Brick(x, y, 4))
                y += brick_length
            x += brick_height
    else:
        #need to add boss level
        pass
    yp = random.randint(0, Screen_width - paddle_sizes[1])
    yb = random.randint(yp, yp + paddle_sizes[1])
    newball = Ball(Screen_height - 5, yb, -1, 1)
    newpaddle = Paddle(Screen_height - 4, yp, 1)
    newpaddle.sethold(newball)
    BALLS.append(newball)
    powerups.append(expandpaddle())
    powerups.append(shrinkpaddle())
    powerups.append(doubletrouble())
    powerups.append(fastball())
    powerups.append(thruball())
    powerups.append(paddlegrab())
    return newpaddle


paddle = setnewlevel()


def print_details(played_time):
    stat1 = str("  LIVES: " + str(display.getlives()) +
                "  |  SCORE:" + str(display.get_score()) + " | LEVEL: " + str(display.get_level()))
    stat2 = str("TIME: " + str(played_time))
    stat3 = str("LEFT : A | RIGHT : D | QUIT: Q ")
    lol = Screen_width / 3
    lol = int(lol)
    print(Fore.WHITE + Back.LIGHTRED_EX + Fore.BLACK + Style.BRIGHT +
          stat1.ljust(lol) + stat2.center(lol) + stat3.rjust(lol) + Style.RESET_ALL)
