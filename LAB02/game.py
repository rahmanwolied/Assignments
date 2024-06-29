from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CATCHER_WIDTH = 150
CATCHER_HEIGHT = 30
FALL_SPEED = 2
NUM_DIAMONDS = 10
RETRY_BUTTON_LOCATION = (20, SCREEN_HEIGHT - 50)
PAUSE_BUTTON_LOCATION = (SCREEN_WIDTH/2, SCREEN_HEIGHT - 50)
EXIT_BUTTON_LOCATION = (SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50)


# Colors
WHITE = (1.0, 1.0, 1.0)
RED = (1.0, 0.0, 0.0)
TEAL = (0.0, 1.0, 1.0)
AMBER = (1.0, 0.5, 0.0)
GREEN = (0.0, 1.0, 0.0)
BLUE = (0.0, 0.0, 1.0)
PURPLE = (1.0, 0.0, 1.0)
YELLOW = (1.0, 1.0, 0.0)
colors = [RED, TEAL, AMBER, GREEN, BLUE, PURPLE, YELLOW]


# initial state
game_over = False
paused = False
exit_game = False

catcher_color = WHITE
retry_color = TEAL
pause_color = AMBER
exit_color = RED

catcher_x = SCREEN_WIDTH / 2
catcher_y = 30
diamond_x = random.randint(0, SCREEN_WIDTH)
diamond_y = SCREEN_HEIGHT - 10

diamonds = []
falling_diamond = None
current_fall_speed = FALL_SPEED
score = 0

# draw functions
def draw_retry_button(x, y, color = retry_color):
    draw_line(x, y, x + 20, y - 20, color)
    draw_line(x, y, x + 20, y + 20, color)
    draw_line(x, y, x + 50, y, color)

def draw_pause_button(x, y, color = pause_color):
    draw_line(x + 10, y + 20, x + 10, y - 20, color)
    draw_line(x - 10, y + 20, x - 10, y - 20, color)

def draw_play_button(x, y, color = pause_color):
    draw_line(x - 10, y + 20, x - 10, y - 20, color)
    draw_line(x - 10, y + 20, x + 10, y, color)
    draw_line(x - 10, y - 20, x + 10, y, color)

def draw_exit(x, y, color = exit_color):
    draw_line(x - 10, y + 10, x + 10, y - 10, color)
    draw_line(x - 10, y - 10, x + 10, y + 10, color)

def draw_diamond(x, y, color):
    width = 15/2
    height = 30/2
    
    draw_line(x, y, x - width, y + height, color)
    draw_line(x, y, x + width, y + height, color)
    draw_line(x, y + (2*height), x - width, y + height, color)
    draw_line(x, y + (2*height), x + width, y + height, color)

def draw_catcher():
    x1, x2 = catcher_x - CATCHER_WIDTH / 2, catcher_x + CATCHER_WIDTH / 2
    x3, x4 = x1 + 20, x2 - 20
    y1, y2 = catcher_y, catcher_y - 20
    
    draw_line(x1, y1, x2, y1, catcher_color)
    draw_line(x3, y2, x4, y2, catcher_color)
    draw_line(x2, y1, x4, y2, catcher_color)
    draw_line(x1, y1, x3, y2, catcher_color)


# animate functions
def animate(v):
    global falling_diamond, score, catcher_x, game_over, catcher_color, current_fall_speed, paused
    
    if not game_over and not paused:
        if not falling_diamond:
            # If there's no currently falling diamond and there are diamonds left
            if diamonds:
                falling_diamond = diamonds.pop(0)

        # If there's a currently falling diamond, update its position
        if falling_diamond:
            diamond_x, diamond_y, diamond_color = falling_diamond
            diamond_y -= current_fall_speed
            falling_diamond = (diamond_x, diamond_y, diamond_color)

            if collision(diamond_y, diamond_x, catcher_x):
                handle_collision()

            # Game over when a diamond is missed
            elif diamond_y < 0:
                game_over = True
                falling_diamond = None
                catcher_color = RED
                current_fall_speed = FALL_SPEED
                print("Game Over! Score:",score)

    if exit_game:
        glutLeaveMainLoop()
    
    glutPostRedisplay()
    glutTimerFunc(10, animate, 0)

# main display function
def display():
    glClear(GL_COLOR_BUFFER_BIT)

    draw_catcher()
    
    if falling_diamond:
        x, y, color = falling_diamond
        draw_diamond(x, y, color)
    
    draw_retry_button(RETRY_BUTTON_LOCATION[0], RETRY_BUTTON_LOCATION[1])
    draw_exit(EXIT_BUTTON_LOCATION[0], EXIT_BUTTON_LOCATION[1])
    
    if not paused: draw_pause_button(PAUSE_BUTTON_LOCATION[0], PAUSE_BUTTON_LOCATION[1])
    else: draw_play_button(PAUSE_BUTTON_LOCATION[0], PAUSE_BUTTON_LOCATION[1])
    
    glutSwapBuffers()

# input handler
def handle_mouse(button, state, x, y):
    global paused, exit_game
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        # handle restart button click
        if x >= RETRY_BUTTON_LOCATION[0] and x <= RETRY_BUTTON_LOCATION[0] + 50:
            y = SCREEN_HEIGHT - y
            if y >= (RETRY_BUTTON_LOCATION[1] - 20)  and y <= (RETRY_BUTTON_LOCATION[1] + 20):
                print("Retry")
                handle_retry()
        # handle pause button click
        elif x >= PAUSE_BUTTON_LOCATION[0] - 10 and x <= PAUSE_BUTTON_LOCATION[0] + 10:
            y = SCREEN_HEIGHT - y
            if y >= (PAUSE_BUTTON_LOCATION[1] - 20)  and y <= (PAUSE_BUTTON_LOCATION[1] + 20):
                if not paused: print("Paused")
                else: print("Play")
                paused = not paused
        
        # handle EXIT button click
        elif x >= EXIT_BUTTON_LOCATION[0] - 10 and x <= EXIT_BUTTON_LOCATION[0] + 10:
            y = SCREEN_HEIGHT - y
            if y >= (EXIT_BUTTON_LOCATION[1] - 10)  and y <= (EXIT_BUTTON_LOCATION[1] + 10):
                exit_game = True

def handle_keyboard(key, x, y):
    global catcher_x
    speed = 20
    if key == GLUT_KEY_LEFT and not game_over and not paused:
        catcher_x -= speed
        if catcher_x < CATCHER_WIDTH / 2:
            catcher_x = CATCHER_WIDTH / 2

    elif key == GLUT_KEY_RIGHT and not game_over and not paused:
        catcher_x += speed
        if catcher_x > SCREEN_WIDTH - CATCHER_WIDTH / 2:
            catcher_x = SCREEN_WIDTH - CATCHER_WIDTH / 2

# event handler
def handle_retry ():
    global score, lives, game_over, catcher_color, falling_diamond, paused

    paused = False
    score = 0
    lives = 1
    game_over = False
    catcher_color = WHITE
    diamonds.clear()
    falling_diamond = None

    for _ in range(NUM_DIAMONDS):
        generate_diamond()

def collision(diamond_y, diamond_x, catcher_x):
    return diamond_y <= CATCHER_HEIGHT and abs(diamond_x - catcher_x) < CATCHER_WIDTH / 2

def handle_collision():
    global score, falling_diamond, current_fall_speed

    score += 1
    print("Score:",score)
    falling_diamond = None
    current_fall_speed += 0.5

# diamond generator
def generate_diamond():
    if not game_over:
        new_diamond_x = random.randint(15, SCREEN_WIDTH - 15)
        new_diamond_y = SCREEN_HEIGHT - 15
        color = random.choice(colors)  # Choose a random color
        diamonds.append((new_diamond_x, new_diamond_y, color))


# MidPoint Line Drawing Algorithm
def draw_points(x, y, color = (1, 1, 1), size=2):
    glColor3fv(color)
    glPointSize(size) 
    glBegin(GL_POINTS)
    glVertex2f(x,y) 
    glEnd()

def to_zone0(zone, x, y):
    if zone == 0: return (x,y)
    elif zone == 1: return (y,x)
    elif zone == 2: return (y,-x)
    elif zone == 3: return (-x,y)
    elif zone == 4: return (-x,-y)
    elif zone == 5: return (-y,-x)
    elif zone == 6: return (-y,x)
    elif zone == 7: return (x,-y)
    else: raise ValueError("Zone must be in [0, 7]")

def to_zoneM(zone, x, y):
    if zone == 0: return (x,y)
    elif zone == 1: return (y,x)
    elif zone == 2: return (-y,x)
    elif zone == 3: return (-x,y)
    elif zone == 4: return (-x,-y)
    elif zone == 5: return (-y,-x) 
    elif zone == 6: return (y,-x)
    elif zone == 7: return (x,-y)
    else: raise ValueError("Zone must be in [0, 7]")

def find_zone(x1,y1,x2,y2):
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) > abs(dy):
        if dx>=0 and dy>=0: return 0
        elif dx>=0 and dy<=0: return 7
        elif dx<=0 and dy>=0: return 3
        elif dx<=0 and dy<=0: return 4
    else :
        if dx>=0 and dy>=0: return 1
        elif dx<=0 and dy>=0: return 2
        elif dx<=0 and dy<=0: return 5
        elif dx>=0 and dy<=0: return 6

def draw_line(x1, y1, x2, y2, color):
    zone = find_zone(x1,y1,x2,y2)
    x1,y1 = to_zone0(zone, x1, y1)
    x2,y2 = to_zone0(zone, x2, y2)
    
    dx = x2 - x1
    dy = y2 - y1
    
    d = 2*dy - dx
    incrE = 2*dy
    incrNE = 2*(dy - dx)

    x = x1
    y = y1
    x0, y0 = to_zoneM(zone, x, y)
    
    draw_points(x0, y0, color)
    while x < x2:
        if d <= 0:
            d = d + incrE
            x = x + 1
        else:
            d = d + incrNE
            x = x + 1
            y = y + 1
        x0, y0 = to_zoneM(zone, x, y)
        
        draw_points(x0, y0, color)


# main function
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(SCREEN_WIDTH, SCREEN_HEIGHT)
    glutCreateWindow(b"Catch the Diamonds")

    # Initialize OpenGL
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT, -1, 1)
    glMatrixMode(GL_MODELVIEW)

    # Register callback functions
    glutDisplayFunc(display)
    glutTimerFunc(10, animate, 0)
    glutSpecialFunc(handle_keyboard)
    glutMouseFunc(handle_mouse)

    for _ in range(NUM_DIAMONDS):
        generate_diamond()
    
    glutMainLoop()

if __name__ == "__main__":
    main()