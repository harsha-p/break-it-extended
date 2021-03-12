import time
from functions import *
from screen import display

start_time = time.time()
screen_time = time.time()
level_start = time.time()
level_time = 0
os.system('clear')

while True:

    print("\033[%d;%dH" % (0, 0))
    time_played = round(time.time()) - round(start_time)
    level_time = round(time.time()) - round(level_start)
    if time.time() - screen_time >= 0.1:
        display.create_screen()
        screen_time = time.time()
        paddle.show()
        # paddle.display([[paddle.getshape()]*paddle_sizes[paddle.gettype()]])
        print_details(time_played)
        if level_time >= 5:
            display.move_down(True)
        check_level = True
        for brick in bricks:
            brick.checkcollision()
            check_level = check_level and (brick.gettype() == 0)
        if display.get_change_level() or check_level:
            display.next_level()
            level_start = time.time()
            paddle = setnewlevel()
        checkpowerups()
        checkbullets()
        for power in powerups:
            power.activate(paddle)
        for ball in BALLS:
            ball.checkcollision(paddle)

        char = input_to(Get())
        if char == 'q' or char == 'Q':
            display.quit()
        elif char == 'd' or char == 'D':
            paddle.moveright()
        elif char == 'a' or char == 'A':
            paddle.moveleft()
        elif char == 'n' or char == 'N':
            display.next_level()
            level_start = time.time()
            paddle = setnewlevel()
        elif char == 's' or char == 'S':
            paddle.shoot()
        elif char == ' ':
            if len(paddle.gethold()) > 0:
                paddle.release()
        display.print_screen()
