from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

# Global Variables
SCREEN_W = 500
SCREEN_H = 500

points = []
colors = []

ballx = bally = 0
ball_size = 5
speed= 0.01

create_new= False
bg_color = (0,0,0)

blink_duration = 1000
blinked = False
last_blinked = 0

frozen = False

def convert_coordinate(x, y):
    global SCREEN_W,SCREEN_H
    a = x - (SCREEN_W / 2)
    b = (SCREEN_H / 2) - y
    return a,b

def draw_points(points,s):
    glPointSize(s)
    for x, y, color in points:
        glBegin(GL_POINTS)
        glColor3f(color[0],color[1],color[2])
        glVertex2f(x,y)
        glEnd()

def keyboardListener(key, x,y):
    global ball_size,frozen
    if key == b' ':
        frozen = not frozen
    glutPostRedisplay()

def specialKeyListener(key,x, y):
    global speed,frozen
    if key == GLUT_KEY_UP:
        speed *= 2
    if key == GLUT_KEY_DOWN:
        speed = speed / 2
    if speed < 0.05:
        speed = 0.05
    glutPostRedisplay()

def mouseListener(key, direction, x, y):
    global points, frozen, blinked, last_blinked, colors
    if key == GLUT_RIGHT_BUTTON and direction == GLUT_DOWN and frozen == False:
        color = (random.uniform(0,1), random.uniform(0,1), random.uniform(0,1))
        c_X,c_y = convert_coordinate(x,y)
        points.append((c_X, c_y, color))

    if key == GLUT_LEFT_BUTTON and direction == GLUT_DOWN and frozen == False:
        blinked = not blinked
        last_blinked = time.time()
        for i in range(len(points)):
            color = points[i][2]
            colors.append(color)
            points[i]= (points[i][0], points[i][1], bg_color)

def check_blink():
    global points, colors, blinked, last_blinked
    if time.time() > last_blinked + 1 and blinked:
        blinked = not blinked
        for i in range(len(points)):
            color = colors[i]
            points[i] =(points[i][0], points[i][1], color)
        glutPostRedisplay()

def showScreen():
    global ball_size
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 200, 0, 0, 0, 0, 1, 0)
    glMatrixMode(GL_MODELVIEW)
    
    draw_points(points,ball_size)
    check_blink()
    glutSwapBuffers()

def animate():
    global frozen, points, speed
    if not frozen:
        for ballx, bally, color in points:
            new_ballx = ballx + random.choice([-10,10])*speed
            new_bally = bally + random.choice([-10,10])*speed
            points[points.index((ballx,bally,color))] = (new_ballx,new_bally,color)
    glutPostRedisplay()

def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104, 1, 1, 1000.0)

def main():
    glutInit()
    glutInitWindowSize(SCREEN_W, SCREEN_H)
    glutInitWindowPosition(0, 0)
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)

    wind = glutCreateWindow(b"OpenGL Coding")
    init()
    glutDisplayFunc(showScreen)
    glutIdleFunc(animate)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutMainLoop()

if __name__ == '__main__':
    main()
