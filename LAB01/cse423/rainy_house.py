from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import random
import time
import math

SCREEN_H = 700
SCREEN_W = 1000

rain_drop_count = 100
# rain_points = [(random.randint(0,SCREEN_W),random.randint(SCREEN_H,SCREEN_H+200), random.randint(30,60)) for _ in range(rain_drop_count)]
rain_points = [( random.randint(0,SCREEN_W), random.randint(SCREEN_H,SCREEN_H+200), random.randint(30,60) )]
rain_direction_vertical = 'DOWN'
rain_skew = 0
rain_speed_horizontal = 2
rain_speed = [10,rain_speed_horizontal]
time_interval = 1
last_rain_time = time.time()
last_time_day = time.time()
day = True
color = 1

def change_time():
    global day
    day = not day

def set_day():
    global day,color, last_time_day
    change = False
    if day:
        if color < 1 and time.time() > last_time_day + 0.05:
            last_time_day = time.time()
            color += 0.01
            change = True
    else:
        if color > 0 and time.time() > last_time_day + 0.05 :
            last_time_day = time.time()
            color -= 0.01
            change = True
    if color < 0:
        color = 0
        change = True
    
    if change:
        glClearColor(color,color,color,color)
        glutPostRedisplay()
        
def keyboardListener(key,x,y):
    if key == b'w':
        print('time changed to', day)
        change_time()

def specialKeyListener(key, x, y):
    global rain_direction_vertical,rain_skew, day
    
    if key==GLUT_KEY_UP:
        rain_direction_vertical = 'UP'
        print("Rain Direction Changed to UP")
    if key== GLUT_KEY_DOWN:	
        rain_direction_vertical = 'DOWN'
        print("Rain Direction Changed to DOWN")
    if key==GLUT_KEY_LEFT and rain_skew > -50:
        rain_skew -= 0.1
    if key== GLUT_KEY_RIGHT and rain_skew < 50:	
        rain_skew += 0.1

    glutPostRedisplay()

def draw_house(starting_x, starting_y,base,height,roof_height,roof_base,scale=15):
    global color
    # Draw the roof
    glColor3f(0.1, 0.5, 0.0)
    draw_triangle(starting_x, starting_y, base=roof_base,height=roof_height, hollow=True ,scale=scale, color=color)
    
    glColor3f(0.1, 0.5, 0.0)
    # Draw the house
    x1,y1 = int(starting_x - (roof_base/2)) + int((roof_base-base)/2) , starting_y-roof_height
    x2,y2 = x1,y1-height
    x3,y3 = x2+base, y2
    x4,y4 = x3, y1
    
    draw_box(x1,y1,x2,y2,x3,y3,x4,y4,10)
    
    # draw the door
    door_height = int(height/2)
    door_width = int(base/5)
    door_x1 = int(x1 + (base/4) - (door_width/2))
    draw_box(door_x1, y2, door_x1, y2+door_height, door_x1+door_width, y2+door_height, door_x1+door_width, y2)
    draw_points(door_x1+door_width-20, y2+int(door_height/2))
    
    #draw Window
    window_height = int(base/6)
    window_width = int(base/6)
    
    window_x1 = int(x3 - (base/4) - (window_width/2))
    window_y1 = y2+door_height+10
    draw_box(window_x1, window_y1, window_x1, window_y1+window_height, window_x1+window_width, window_y1+window_height, window_x1+window_width, window_y1)
    draw_line(window_x1+window_width/2, window_y1, window_x1+window_width/2, window_y1+window_height,2)

def add_rain_point():
    global rain_drop_count,rain_points,time_interval,last_rain_time
    now = time.time()
    if now > last_rain_time + time_interval and len(rain_points) < rain_drop_count:
        print(len(rain_points))
        last_rain_time = now
        rain_points.append((random.randint(0,SCREEN_W),random.randint(SCREEN_H,SCREEN_H+200), random.randint(30,60)))

def rain(speed):
    global x,rain_direction_vertical, time,rain_skew, time_interval
    if rain_direction_vertical == 'UP': speed[0] = -speed[0]
    last_time = time.time()
    if time.time() > last_time + 0.01 and time_interval > 0.3:
        time_interval -= 0.5

    for x,y,h in rain_points:
        new_y = (y - speed[0])
        new_x = x + speed[1] * (rain_skew/abs(rain_skew)) if rain_skew != 0 else x

        if rain_direction_vertical == "DOWN" and new_y < SCREEN_H/1.5:
            new_y = SCREEN_H

        elif rain_direction_vertical == "UP" and new_y > SCREEN_H:
            new_y = SCREEN_H/1.5

        if new_x < 0:
            new_x = SCREEN_W

        elif new_x > SCREEN_W:
            new_x = 0

        rain_points[rain_points.index((x,y,h))] = (new_x,new_y,h)
    glutPostRedisplay()
    
    
def iterate():
    glViewport(0, 0, SCREEN_W, SCREEN_H)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 1000, 0.0, 700, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def draw_rain(x,y,h):
    global rain_skew
    if rain_skew == 0:
        draw_line(x,y,x,y+h,2)
    else:
        x2 = int(math.atan(rain_skew) * h)
        draw_line(x,y,x-x2,y+h,2)

def showScreen():
    global x,rain_skew, rain_drop_count,day
    add_rain_point()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # glTranslatef(0.0,0.0,0)

    glColor3f(0.0, 0.0, 0.0) #konokichur color set (RGB)
    
    #call the draw methods here
    glColor3f(0.0, 0.0, 1.0)
    for x,y,h in rain_points:
        draw_rain(x,y,h)
    
    set_day()
    draw_house(starting_x=SCREEN_W/2, starting_y=600,base=400,height=200,roof_base=500,roof_height=150, scale=10)
    
    glutSwapBuffers()

def init():
    #//clear the screen
    glClearColor(1,1,1,1);
    #//load the PROJECTION matrix
    glMatrixMode(GL_PROJECTION)
    #//initialize the matrix
    glLoadIdentity()
    #//give PERSPECTIVE parameters
    gluPerspective(504,	1,	1,	1000.0)
    # **(important)**aspect ratio that determines the field of view in the X direction (horizontally). The bigger this angle is, the more you can see of the world - but at the same time, the objects you can see will become smaller.

def draw_points(x, y):
    glPointSize(5) #pixel size. by default 1 thake
    glBegin(GL_POINTS)
    glVertex2f(x,y) #jekhane show korbe pixel
    glEnd()

def draw_line(x1,y1,x2,y2, w=5):
    glLineWidth(w)
    glBegin(GL_LINES)
    glVertex2f(x1,y1)
    glVertex2f(x2,y2)
    glEnd()

def draw_box(x1,y1,x2,y2,x3,y3,x4,y4,w=5):
    glLineWidth(w)
    glBegin(GL_LINES)
    
    # left
    glVertex2f(x1,y1)
    glVertex2f(x2,y2)
    
    #bottom
    glVertex2f(x2,y2)
    glVertex2f(x3,y3)
    
    #right
    glVertex2f(x3,y3)
    glVertex2f(x4,y4)
    
    #top
    glVertex2f(x4,y4)
    glVertex2f(x1,y1)
    
    glEnd()

def draw_quad(x1,y1,x2,y2,x3,y3,x4,y4):
    glBegin(GL_QUADS)
    glVertex2f(x1,y1)
    glVertex2f(x2,y2)
    glVertex2f(x3,y3)
    glVertex2f(x4,y4)
    glEnd()
    
def draw_triangle(starting_x, starting_y, base,height, hollow=False,scale=5, color=1.0):
    x1,y1 = starting_x, starting_y
    x2,y2 = int(x1 - (base/2)), y1 - height
    x3,y3 = int(x1 + (base/2)), y1 - height
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(x1,y1)   #left
    glVertex2f(x2,y2)   #top
    glVertex2f(x3,y3)   #right
    glEnd()     
    if hollow:
        center_y = y1 - int(height/2)
        scale = 1.2
        base = int(base * (1/scale) )
        height = int(height * (1/scale) )
        y1 = center_y + int(height/2)
        x2,y2 = int(x1 - (base/2)), y1 - height
        x3,y3 = int(x1 + (base/2)), y1 - height
    
        # draw a smaller triangle inside the larger one
        glColor3f(color, color, color)
        glBegin(GL_TRIANGLE_FAN)
        
        glVertex2f(x1,y1)  
        glVertex2f(x2,y2)         
        glVertex2f(x3,y3)   
        glEnd()  
        glColor3f(0.0, 0.0, 0.0)
        
        # draw_line(x1,y1,x2,y2,scale)
        # draw_line(x2,y2,x3,y3,scale)
        # draw_line(x1,y1,x3,y3,scale)

def main():
    glutInit()
    glutInitWindowSize(1000, 700) #window size
    glutInitWindowPosition(0, 0)
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)

    wind = glutCreateWindow(b"OpenGL Coding Practice") #window name
    init()

    glutDisplayFunc(showScreen)
    glutSpecialFunc(specialKeyListener)
    glutKeyboardFunc(keyboardListener)
    glutIdleFunc(lambda: rain(rain_speed))

    glutMainLoop()

if __name__ == '__main__':
    main()