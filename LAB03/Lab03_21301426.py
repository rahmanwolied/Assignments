from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GROW_SPEED = 0.5
RADIUS = 100

# initializing variables and flags
paused = False
circles = []
current_grow_speed = GROW_SPEED

# animate functions
def animate(v):
    global paused, circles, current_grow_speed       

    if not paused:
        for i in range(len(circles)):
            if i >= len(circles): break
            radius, x, y = circles[i]
            radius += current_grow_speed
            if collision(radius, x, y):
                circles.pop(i)
                continue
            circles[i] = (radius, x, y)
    
    glutPostRedisplay()
    glutTimerFunc(10, animate, 0)

# main display function
def display():
    glClear(GL_COLOR_BUFFER_BIT)
    
    for radius, x, y in circles:
        draw_circle(radius, (x, y))

    glutSwapBuffers()

# input handler
def handle_mouse(button, state, x, y):
    global paused, circles
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN and not paused:
        y = SCREEN_HEIGHT - y
        circles.append((RADIUS,x, y))

def handle_keyboard(key, x, y):
    global current_grow_speed, paused
    speed = 0.3
    if key == GLUT_KEY_LEFT and not paused:
        print("Speed is increased")
        current_grow_speed += speed

    elif key == GLUT_KEY_RIGHT and not paused:
        print("Speed is decreased")
        current_grow_speed -= speed
        if current_grow_speed < 0: current_grow_speed = 0
    if key == b' ':
        paused = not paused
        if paused:
            print("Game Paused")
        else:
            print("Game Resumed")

# event handler
def collision(radius, center_x, center_y):
    return (center_x - radius <= 0 or center_x + radius >= SCREEN_WIDTH or center_y - radius <= 0 or center_y + radius >= SCREEN_HEIGHT)

# MidPoint Circle Drawing Algorithm
def draw_points(x, y, color = (1, 1, 1), size=2):
    glColor3fv(color)
    glPointSize(size) 
    glBegin(GL_POINTS)
    glVertex2f(x,y) 
    glEnd()

def to_zoneM(zone, x, y):
    if zone == 1: return (x,y)
    elif zone == 6: return (x,-y)
    elif zone == 5: return (-x,-y) 
    elif zone == 2: return (-x,y)
    elif zone == 0: return (y,x)
    elif zone == 3: return (-y,x)
    elif zone == 4: return (-y,-x)
    elif zone == 7: return (y,-x)
    else: raise ValueError("Zone must be in [0, 7]")

def draw_circle(r, center):
    d = 1-r
    x = 0
    y = r

    incrE = (2 * x) + 3
    incrSE = (2 * x) - (2 * y) + 5

    while x < y:
        if d < 0:
            d = d + incrE
            x = x + 1
        else:
            d = d + incrSE
            x = x + 1
            y = y - 1
        if x > y: break

        for i in range(8):
            x_, y_ = to_zoneM(i, x, y)
            draw_points(x_ + center[0], y_ + center[1])

        incrE = (2 * x) + 3
        incrSE = (2 * x) - (2 * y) + 5

# main function
def main():
    glutInit(sys.argv)
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
    glutKeyboardFunc(handle_keyboard)
    glutMouseFunc(handle_mouse)
    
    glutMainLoop()

if __name__ == "__main__":
    main()