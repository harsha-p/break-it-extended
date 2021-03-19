import time
from functions import *
from input import *
from screen import display

start_time = time.time()
screen_time = time.time()
level_start = time.time()
level_time = 0
shoot_interval = 0
os.system('clear')
setnewlevel()

while True:

    print("\033[%d;%dH" % (0, 0))
    time_played = round(time.time()) - round(start_time)
    level_time = round(time.time()) - round(level_start)
    if time.time() - screen_time >= 0.05:
        boss = display.get_boss()
        paddle = display.get_paddle()
        display.create_screen()
        screen_time = time.time()
        display.get_paddle().show()
        if boss:
            boss.show()
        print_details(time_played)
        if level_time >= 5:
            display.move_down(True)
        check_level = True
        for brick in bricks:
            brick.check_collision()
            check_level = check_level and (brick.gettype() == 0)
        if display.get_change_level() or (check_level and display.get_level() != 0):
            display.next_level()
            level_start = time.time()
            paddle = setnewlevel()
        check_powerups()
        check_bullets()
        for power in powerups:
            power.activate()
        for ball in BALLS:
            ball.check_collision()

        if time.time() - shoot_interval >= 1:
            shoot_interval = time.time()
            paddle.shoot()
        display.print_screen()

    char = input_to(Get())
    if char == 'q' or char == 'Q':
        display.quit()
    elif char == 'd' or char == 'D':
        paddle.move_right()
    elif char == 'a' or char == 'A':
        paddle.move_left()
    elif char == 'n' or char == 'N':
        display.next_level()
        level_start = time.time()
        paddle = setnewlevel()
    elif char == '.':
        if boss:
            boss.shoot()
    # elif char == 's' or char == 'S':
    #     if time.time() - shoot_interval >= 0.5:
    #         shoot_interval = time.time()
    #         paddle.shoot()
    elif char == ' ':
        if len(paddle.get_hold()) > 0:
            paddle.release()
