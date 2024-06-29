from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
W_Width,W_Height=500, 500
store=[]
points= []
ballx=bally= 0
ball_size= 5
speed= 0.01
create_new= False
background_color= (0,0,0)
blink_duration=800
freeze=False
def convert_coordinate(x, y):
    global W_Width,W_Height
    a =x-(W_Width/2)
    b = (W_Height /2)-y
    return a,b

def draw_points(points,s):
    glPointSize(s)
    for x, y,color in points:
        glBegin(GL_POINTS)
        glColor3f(color[0],color[1],color[2])
        glVertex2f(x,y)
        glEnd()

def keyboardListener(key, x,y):
    global ball_size,freeze
    if key== b' ':
        freeze= not freeze
    glutPostRedisplay()

def specialKeyListener(key,x, y):
    global speed,freeze
    if key== GLUT_KEY_UP:
        speed *= 2
    if key== GLUT_KEY_DOWN:
        speed = max(speed / 2, 0.005)
    glutPostRedisplay()

def mouseListener(button, state, x, y):
    global points,store, freeze
    if button== GLUT_RIGHT_BUTTON and state== GLUT_DOWN and freeze==False:
        color=(random.uniform(0,1), random.uniform(0,1), random.uniform(0,1))
        c_X,c_y =convert_coordinate(x,y)
        points.append((c_X,c_y,color))

    if button== GLUT_LEFT_BUTTON and state== GLUT_DOWN and freeze==False:
        blink_timer= int(blink_duration )
        for i in range(len(points)):
            r,g,b = points[i][2]
            store.append((r,g,b))
            points[i]= (points[i][0], points[i][1], background_color)
        glutTimerFunc(blink_timer, blink, 0)

def blink(value):
    global points,store
    for i in range(len(points)):
        r,g,b= store[i]
        points[i] =(points[i][0],points[i][1],(r,g,b))
    glutPostRedisplay()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 200, 0, 0, 0, 0, 1, 0)
    glMatrixMode(GL_MODELVIEW)
    global ball_size
    draw_points(points,ball_size)
    glutSwapBuffers()

def animate():
    global freeze
    if freeze==False:
        glutPostRedisplay()
        global points, speed
        new_points = []  
        for ballx, bally, color in points:
            ballx = (ballx + random.choice([-10,10])*speed)
            bally = (bally + random.choice([-10,10])*speed)
            new_points.append((ballx, bally, color))  
        points = new_points 

def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104, 1, 1, 1000.0)

glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)

wind = glutCreateWindow(b"OpenGL Coding")
init()
glutDisplayFunc(display)
glutIdleFunc(animate)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glutMainLoop()


