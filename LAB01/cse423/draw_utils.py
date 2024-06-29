from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

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