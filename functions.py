from objects import *
from input import *
from headers import *


def checkpowerups():
    i = 0
    while i < len(newpowerups):
        if newpowerups[i].check():
            newpowerups.pop(i)
        else:
            i += 1


def checkbullets():
    i = 0
    while i < len(bullets):
        if bullets[i].checkcollision():
            bullets.pop(i)
        else:
            i += 1


def setnewlevel():
    x = 4
    bricks.clear()
    BALLS.clear()
    powerups.clear()
    newpowerups.clear()
    yp = random.randint(0, Screen_width - paddle_sizes[1])
    yb = random.randint(yp, yp + paddle_sizes[1] - 1)
    newball = Ball(Screen_height - 5, yb, -1, 1)
    newpaddle = Paddle(Screen_height - 4, yp, 1)
    newpaddle.sethold(newball)
    BALLS.append(newball)
    display.set_paddle(newpaddle)
    if display.get_level() <= 3 and display.get_level() > 0:
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
        x = 16
        while x < Screen_height - 10:
            y = 6
            while y + brick_length <= Screen_width - 6:
                if random.randint(1, 100) <= 10:
                    bricks.append(Brick(x, y, 4))
                y += brick_length
            x += brick_height
        boss = Ufo(newpaddle.gety())
        display.set_boss(boss)
        return
    powerups.append(expandpaddle())
    powerups.append(shrinkpaddle())
    powerups.append(doubletrouble())
    powerups.append(fastball())
    powerups.append(thruball())
    powerups.append(paddlegrab())
    powerups.append(shootpaddle())


def print_details(played_time):
    stat = str(" LIVES: " + str(display.getlives()) +
               "  |  SCORE:" + str(display.get_score()) + " | LEVEL: " + str(display.get_level()))
    time_palyed = str(" | TIME: ") + str(played_time) + " | "
    powerup_stat = "| "
    for pup in powerups:
        powerup_stat += str(pup.name) + ": " + str(pup.gettimer() // 10) + str(" | ")
    controls = str("LEFT : A | RIGHT : D | SHOOT: S | SKIP LEVEL : N | QUIT: Q ")
    print(Fore.WHITE + Back.LIGHTRED_EX + Fore.BLACK + Style.BRIGHT + (stat + time_palyed + controls).center(
        Screen_width) + Style.RESET_ALL)
    print(
        Fore.WHITE + Back.LIGHTRED_EX + Fore.BLACK + Style.BRIGHT + powerup_stat.center(Screen_width) + Style.RESET_ALL)
