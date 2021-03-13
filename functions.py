from paddle import *
from ufo import *

def check_powerups():
    i = 0
    while i < len(new_powerups):
        if new_powerups[i].check():
            new_powerups.pop(i)
        else:
            i += 1


def check_bullets():
    i = 0
    while i < len(bullets):
        if bullets[i].check_collision():
            bullets.pop(i)
        else:
            i += 1


def setnewlevel():
    x = 4
    bricks.clear()
    BALLS.clear()
    powerups.clear()
    new_powerups.clear()
    yp = random.randint(0, Screen_width - paddle_sizes[1])
    yb = random.randint(yp, yp + paddle_sizes[1] - 1)
    new_ball = Ball(Screen_height - 5, yb, -1, 1)
    new_paddle = Paddle(Screen_height - 4, yp, 1)
    new_paddle.set_hold(new_ball)
    BALLS.append(new_ball)
    display.set_paddle(new_paddle)
    if 3 >= display.get_level() > 0:
        while x < Screen_height - 16:
            y = 6
            while y + brick_length <= Screen_width - 6:
                if random.randint(1, 100) <= display.get_level() * 20:
                    if random.randint(1, 10) <= 9:
                        bricks.append(Brick(x, y, random.randint(1, 3)))
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
        boss = Ufo(new_paddle.gety())
        display.set_boss(boss)
        return
    powerups.append(expandpaddle())
    powerups.append(ShrinkPaddle())
    powerups.append(DoubleTrouble())
    powerups.append(FastBall())
    powerups.append(ThruBall())
    powerups.append(PaddleGrab())
    powerups.append(ShootPaddle())


def print_details(played_time):
    stat = str(" LIVES: " + str(display.get_paddle().get_lives()) +
               "  |  SCORE:" + str(display.get_score()) + " | LEVEL: " + str(display.get_level()))
    time_played = str(" | TIME: ") + str(played_time) + " | "
    power_stat = ""

    for pup in powerups:
        power_stat += str(pup.name) + ": " + str(pup.gettimer() // 10) + str(" | ")

    controls = str("LEFT : A | RIGHT : D | SHOOT: S | SKIP LEVEL : N | QUIT: Q ")

    print(Fore.WHITE + Back.LIGHTRED_EX + Fore.BLACK + Style.BRIGHT + ("| " + stat + time_played + controls).center(
        Screen_width) + Style.RESET_ALL)

    if power_stat != "":
        print(
            Fore.WHITE + Back.LIGHTRED_EX + Fore.BLACK + Style.BRIGHT + power_stat.center(
                Screen_width) + Style.RESET_ALL)

    if display.get_boss():
        history_bar = str(Back.GREEN + " " * (Screen_width // 10) * display.get_boss().get_lives() + Back.WHITE + " " * (
                    Screen_width // 10) * (10 - display.get_boss().get_lives()) + Back.LIGHTRED_EX)

        print(Fore.WHITE + Back.LIGHTRED_EX + Fore.BLACK + Style.BRIGHT + history_bar.center(
            Screen_width) + Style.RESET_ALL)
