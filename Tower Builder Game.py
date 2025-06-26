from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import random
import sys
from OpenGL.GL import *

# Midpoint Line Algorithm

def findZone(x1, y1, x2, y2):
    dy = y2-y1
    dx = x2-x1
    if abs(dx) > abs(dy):
        if dx > 0 and dy > 0:
            return 0
        elif dx < 0 and dy > 0:
            return 3
        elif dx < 0 and dy < 0:
            return 4
        else:
            return 7
    else:
        if dx > 0 and dy > 0:
            return 1
        elif dx < 0 and dy > 0:
            return 2
        elif dx < 0 and dy < 0:
            return 5
        else:
            return 6


def convertzones(x1, y1, zone, to_zero):
    if zone == 0:
        return x1, y1
    elif zone == 1:
        return y1, x1
    elif zone == 2 and to_zero == True:
        return y1, -x1
    elif zone == 2 and to_zero == False:
        return -y1, x1
    elif zone == 3:
        return -x1, y1
    elif zone == 4:
        return -x1, -y1
    elif zone == 5:
        return -y1, -x1
    elif zone == 6 and to_zero == True:
        return -y1, x1
    elif zone == 6 and to_zero == False:
        return y1, -x1
    elif zone == 7:
        return x1, -y1


def midpointlinealgo(x1, x2, y1, y2):
    zone = findZone(x1, y1, x2, y2)

    glVertex2f(x1, y1)

    x1, y1 = convertzones(x1, y1, zone, True)
    x2, y2 = convertzones(x2, y2, zone, True)
    dy = y2 - y1
    dx = x2 - x1
    d = 2 * dy - dx
    while True:
        if x1 == x2 and y1 == y2:
            break
        if d > 0:
            d = d + 2 * dy - 2 * dx
            x1 += 1
            y1 += 1
            x1, y1 = convertzones(x1, y1, zone, False)

            glVertex2f(x1, y1)

            x1, y1 = convertzones(x1, y1, zone, True)
        else:
            d = d + 2 * dy
            x1 += 1
            x1, y1 = convertzones(x1, y1, zone, False)

            glVertex2f(x1, y1)

            x1, y1 = convertzones(x1, y1, zone, True)


# Midpoint Circle Algorithm

def all_circle_zones(x, y, x0, y0):
    glVertex2f(x + x0, y + y0)
    glVertex2f(y + x0, x + y0)
    glVertex2f(y + x0, -x + y0)
    glVertex2f(x + x0, -y + y0)
    glVertex2f(-x + x0, -y + y0)
    glVertex2f(-y + x0, -x + y0)
    glVertex2f(-y + x0, x + y0)
    glVertex2f(-x + x0, y + y0)


def midpointcirclealgo(x1, y1, r = 30):
    d_init = 1 - r
    d = d_init

    x = 0
    y = r
    while x < y:
        all_circle_zones(x, y, x1, y1)
        if d >= 0:
            d = d + 2*x - 2*y + 5
            x += 1
            y -= 1
        else:
            d = d + 2*x + 3
            x += 1

W_Width, W_Height = 500,500

radius = 0
wind = 0
itr = 0
play_hitbox = [(-14, 237), (34, 192)]
cross_hitbox = [(-14+200, 237), (34+200, 192)]
back_hitbox = [(-14-220, 237), (34-200, 192)]
stack = []
curr_bottom_surf = []
stack_top_surf = []
tilt = 0

building1 = 0
building2 = 0

move_x, move_y = 0,0
dir = "left"

game_state = "playing"
game_over = False

current_level = 1

score_value = 0


def store_current():
    global move_x, move_y, game_state

    x1, y1 = -35, 130
    x2, y2 = -35, 180
    x3, y3 = 35, 180
    x4, y4 = 35, 130
    x1 += move_x
    x2 += move_x
    x3 += move_x
    x4 += move_x

    y1 += move_y
    y2 += move_y
    y3 += move_y
    y4 += move_y

    if current_level == 2:
        x1 += 10
        x2 += 10
        x3 -= 10
        x4 -= 10
    elif current_level == 3:
        x1 += 20
        x2 += 20
        x3 -= 20
        x4 -= 20

    store_blocks([(x1, y1), (x2, y2), (x3, y3), (x4, y4)])
    move_y = 0
    move_x = 0
    if game_state == "falling":
        game_state = "playing"

def store_blocks(arr):
    global stack, stack_top_surf
    stack.append(arr)
    if len(stack) > 0:
        stack_top_surf = [stack[-1][1], stack[-1][2]]


def convert_coordinate(x, y):
    global W_Width, W_Height
    a = x - (W_Width/2)
    b = (W_Height/2) - y
    return a,b



def mouseListener(button, state, x, y):
    global game_state,game_over

    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            p, q = convert_coordinate(x, y)
            if p >= play_hitbox[0][0] and p <= play_hitbox[1][0] and q <= play_hitbox[0][1] and q >= play_hitbox[1][1]:
                print(game_state)
                if game_state == "playing":
                    game_state = "pause"
                elif game_state == "pause":
                    game_state = "playing"
            elif p >= cross_hitbox[0][0] and p <= cross_hitbox[1][0] and q <= cross_hitbox[0][1] and q >= cross_hitbox[1][1]:
                glutLeaveMainLoop()
            elif p >= back_hitbox[0][0] and p <= back_hitbox[1][0] and q <= back_hitbox[0][1] and q >= back_hitbox[1][1]:
                restart_game()


    glutPostRedisplay()


def keyboardListener(key, x, y):
    global freeze, speed, game_state,current_level,game_over
    if not game_over:
        if key == b' ':
            if game_state == "playing":
                game_state = "falling"
    elif game_over:
        if key == b'r':
            game_state = "playing"
            restart_game()

    glutPostRedisplay()


def current_block():
    global move_x, move_y, curr_bottom_surf, game_state, current_level

    glBegin(GL_POINTS)
    glColor3f(0, 1, 1)
    x1, y1 = -35, 130
    x2, y2 = -35, 180
    x3, y3 = 35, 180
    x4, y4 = 35, 130

    x1 += move_x
    x2 += move_x
    x3 += move_x
    x4 += move_x

    y1 += move_y
    y2 += move_y
    y3 += move_y
    y4 += move_y

    if current_level == 1:
        midpointlinealgo(x2, x1, y2, y1)
        midpointlinealgo(x3, x4, y3, y4)
        midpointlinealgo(x2, x3, y2, y3)
        midpointlinealgo(x1, x4, y1, y4)
        glEnd()

        curr_bottom_surf = [(x1, y1), (x4, y4)]

    elif current_level == 2:
        x1 += 10
        x2 += 10
        x3 -= 10
        x4 -= 10
        midpointlinealgo(x2, x1, y2, y1)
        midpointlinealgo(x3, x4, y3, y4)
        midpointlinealgo(x2, x3, y2, y3)
        midpointlinealgo(x1, x4, y1, y4)

        glEnd()

        curr_bottom_surf = [(x1, y1), (x4, y4)]


    elif current_level == 3:
        x1 += 20
        x2 += 20
        x3 -= 20
        x4 -= 20

        midpointlinealgo(x2, x1, y2, y1)
        midpointlinealgo(x3, x4, y3, y4)
        midpointlinealgo(x2, x3, y2, y3)
        midpointlinealgo(x1, x4, y1, y4)

        glEnd()

        curr_bottom_surf = [(x1, y1), (x4, y4)]

def generate_wind():
    global wind, current_level

    wind = random.randint(-current_level+1, current_level-1)

def base_block():
    global itr

    if itr == 0:
        glBegin(GL_POINTS)
        glColor3f(0, 1, 1)
        x1, y1 = -35, -250
        x2, y2 = -35, -200
        x3, y3 = 35, -200
        x4, y4 = 35, -250


        if current_level == 2:
            x1 += 10
            x2 += 10
            x3 -= 10
            x4 -= 10

        elif current_level == 3:
            x1 += 20
            x2 += 20
            x3 -= 20
            x4 -= 20

        coords = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
        store_blocks(coords)
        glEnd()
        itr += 1


def draw_stack():
    global stack,current_level

    glBegin(GL_POINTS)
    glColor3f(0, 1, 1)
    for coords in stack:
        x1, y1 = coords[0]
        x2, y2 = coords[1]
        x3, y3 = coords[2]
        x4, y4 = coords[3]

        midpointlinealgo(x2, x1, y2, y1)
        midpointlinealgo(x3, x4, y3, y4)
        midpointlinealgo(x2, x3, y2, y3)
        midpointlinealgo(x1, x4, y1, y4)
    glEnd()


def goal_line():
    glBegin(GL_POINTS)
    glColor3f(1, 0, 0)

    dashed_line = np.linspace(-250, 250, 30)
    dashed_line = np.round(dashed_line).astype(int)

    for i in range(len(dashed_line)-1):
        if i%2 == 0:
            midpointlinealgo(dashed_line[i], dashed_line[i+1], 130, 130)
    glEnd()


def draw_buildings():
    global building1, building2, current_level
    glBegin(GL_POINTS)
    if current_level == 2:
        glColor3f(0, 1, 0.5)
        midpointlinealgo(-180, -180 + building1, -250, -200)
        midpointlinealgo(-140, -140 + building1, -250, -200)
        midpointlinealgo(-180 + building1, -140 + building1, -200, -200)
        midpointlinealgo(-180, -140, -250, -250)
        top_x1 = -180 + building1
        top_x2 = -140 + building1
        top_y = -200
        mid_x = round((top_x1 + top_x2) / 2)

        midpointlinealgo(top_x1, mid_x, top_y, top_y + 20)
        midpointlinealgo(top_x2, mid_x, top_y, top_y + 20)

    elif current_level == 3:
        glColor3f(0, 1, 0.5)
        midpointlinealgo(-180, -180 + building1, -250, -200)
        midpointlinealgo(-140, -140 + building1, -250, -200)
        midpointlinealgo(-180, -140, -250, -250)

        glColor3f(0.5, 1, 0.5)

        midpointlinealgo(-180 + building1, -180 + building1 + building2, -200, -125)
        midpointlinealgo(-140 + building1, -140 + building1 + building2, -200, -125)
        midpointlinealgo(-180 + building1 + building2, -140 + building1 + building2, -125, -125)

        top_x1 = -180 + building1 + building2
        top_x2 = -140 + building1 + building2
        top_y = -125
        mid_x = round((top_x1 + top_x2) / 2)

        midpointlinealgo(top_x1, mid_x, top_y, top_y + 20)
        midpointlinealgo(top_x2, mid_x, top_y, top_y + 20)

    glEnd()



def background():
    glBegin(GL_POINTS)
    glColor3f(139 / 255, 69 / 255, 19 / 255)
    midpointlinealgo(160, 160, 60, 0)
    midpointlinealgo(180, 180, 60, 0)
    midpointlinealgo(167, 167, 60, 0)
    midpointlinealgo(174, 174, 60, 0)

    midpointlinealgo(227, 227, 60, 0)
    midpointlinealgo(220, 220, 60, 0)
    midpointlinealgo(207, 207, 60, 0)
    midpointlinealgo(214, 214, 60, 0)

    glColor3f(0, 1, 0)
    for i in range(10, 30, 4):
        midpointcirclealgo(170, 80, i)
        midpointcirclealgo(217, 80, i)
    glEnd()


def play_button():
    glBegin(GL_POINTS)
    glColor3f(0, 0, 1)
    midpointlinealgo(-10, -10, 237, 193)
    midpointlinealgo(-10, 34, 193, 214)
    midpointlinealgo(34, -10, 214, 237)
    glEnd()


def pause_button():
    glBegin(GL_POINTS)
    glColor3f(0, 0, 1)
    midpointlinealgo(-14, -14, 237, 202)
    midpointlinealgo(14, 14, 237, 202)
    glEnd()


def cross_button():
    glBegin(GL_POINTS)
    glColor3f(0, 1, 0)
    midpointlinealgo(195, 231, 237, 202)
    midpointlinealgo(231, 195, 237, 202)
    glEnd()


def back_button():
    glBegin(GL_POINTS)
    glColor3f(1, 0, 0)
    midpointlinealgo(-216, -241, 237, 215)
    midpointlinealgo(-241, -216, 215, 193)
    midpointlinealgo(-241, -200, 215, 215)
    glEnd()

def draw_score():
    glColor3f(1.0, 1.0, 1.0)
    glRasterPos2f(-250, 0 )
    score_str = "Score: " + str(score_value)
    for char in score_str:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

def draw_game_over():
    glColor3f(1.0, 0.0, 0.0)
    glRasterPos2f(-250,100)
    game_over_str = "Game Over! "
    game_over_str1 = "Press R to Restart"

    for char in game_over_str:
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))
    for char in game_over_str1:
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))

def draw_level():
    global current_level
    glColor3f(0.0, 1.0, 0.0)
    glRasterPos2f(-250,20)
    game_over_str = f"Level {current_level}"

    for char in game_over_str:
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))

def draw_end():
    glColor3f(0.0, 1.0, 1.0)
    glRasterPos2f(-250,100)
    end_str = f"Game End"
    end_str1 = f"Thank you For Playing"

    for char in end_str:
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))
    for char in end_str1:
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))




def draw_wind_dir():
    global wind

    glColor3f(1.0, 1.0, 0.0)
    glRasterPos2f(-250,-20)

    wind_str1 = f"Wind: {abs(wind)} mph" \
                f"<<<"
    wind_str2 = f"Wind: {abs(wind)} mph" \
                f">>>"
    wind_str3 = f"Wind: {abs(wind)} mph"
    if wind == 0:
        for char in wind_str3:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

    if wind < 0:
        for char in wind_str1:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
    if wind > 0:
        for char in wind_str2:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))


def restart_game():
    global current_level, game_over, radius, stack, itr, move_x, move_y, dir, game_state,score_value, building2, building1, tilt
    print("Starting Over")
    current_level = 1
    game_over = False
    radius = 0
    stack = []
    itr = 0
    building1, building2, tilt = 0, 0, 0
    move_x, move_y = 0, 0
    dir = "left"
    game_state = "playing"
    score_value = 0




def move_block(_):
    global move_x, move_y, dir, game_state, curr_bottom_surf, stack_top_surf,score_value, wind, tilt, game_over

    x1 = curr_bottom_surf[0][0]
    x4 = curr_bottom_surf[1][0]
    x2 = stack_top_surf[0][0]
    x3 = stack_top_surf[1][0]
    y4 = curr_bottom_surf[1][1]
    y3 = stack_top_surf[1][1]

    if game_state == "playing":
        initial_speed = current_level * 1
        if dir == "left":
            move_x -= initial_speed
            if move_x < -225:
                dir = "right"
        elif dir == "right":
            move_x += initial_speed
            if move_x > 225:
                dir = "left"

    if game_state == "falling":
        move_x += wind
        if y4 > y3:
            move_y -= 5
        elif y4 <= y3:
            move_y += y3 - y4
            if (x2 >= x1) and (x2 <= x4):
                tilt -= abs(x3 - x4)
                store_current()
                score_value += 1

            elif (x3 >= x1) and (x3 <= x4):
                tilt += abs(x1 - x2)
                store_current()
                score_value += 1
            else:
                game_over = True
                game_state = "over"

        else:
            game_over = True


    glutPostRedisplay()
    glutTimerFunc(5, move_block, 0)


def display():
    global current_level,game_over,radius, game_state, dir, stack, curr_bottom_surf, stack_top_surf, move_y, move_x, itr, wind, tilt, building1, building2
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0,0,0,0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0,0,200,	0,0,0,	0,1,0)
    glMatrixMode(GL_MODELVIEW)

    if game_over:
        glColor3f(1.0, 0.0, 0.0)
        draw_game_over()
    if current_level == 4:
        glColor3f(1.0, 0.0, 0.0)
        draw_end()

    if itr != 0:
        if stack_top_surf[0][1] < 130:
            if game_state == "playing" or game_state == "falling":
                pause_button()
            else:
                play_button()
            if current_level > 1:
                draw_buildings()
            background()
            cross_button()
            back_button()
            goal_line()
            base_block()
            draw_stack()
            current_block()

        else:
            current_level += 1
            radius = 0
            if current_level == 2:
                building1 = round(tilt/3)
            elif current_level == 3:
                building2 = round(tilt / 3)
            tilt = 0
            stack = []
            itr = 0
            move_x, move_y = 0, 0
            dir = "left"
            game_state = "playing"
            game_over = False


    else:
        if game_state == "playing" or game_state == "falling":
            pause_button()
        else:
            play_button()

        if current_level > 1:
            draw_buildings()
        background()
        cross_button()
        back_button()
        goal_line()
        base_block()
        generate_wind()
        draw_stack()
        current_block()
    if current_level != 4:
        draw_level()
        draw_score()
        draw_wind_dir()
    glutSwapBuffers()


def init():
    glClearColor(0,0,0,0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104,	1,	1,	1000.0)


glutInit()
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Tower Construction Game")
init()
glutDisplayFunc(display)

glutTimerFunc(100, move_block, 0)

glutKeyboardFunc(keyboardListener)
glutMouseFunc(mouseListener)
glutMainLoop()
