from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
import numpy as np

WINDOW_WIDTH = 288
WINDOW_HEIGHT = 512

def pipe(width,height,direction,posx = 0,posy = 0):
    # im = np.array(Image.open("resources/sprites/pipe-red.png"))
    im = np.array(Image.open('resources/sprites/photo-1472214103451-9374bd1c798e.jpg'))[::-1]
    # im = np.full( (height,width,3),100,dtype=np.uint)
    # print(im)
    # glRasterPos2d(posx,posy)
    print(im.shape)
    glWindowPos2d(posx,posy)
    glDrawPixels(im.shape[1],im.shape[0],  GL_RGB ,GL_UNSIGNED_BYTE,im)
    # glBitmap(128,500,  GL_RGBA ,GL_UNSIGNED_BYTE,im)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glBegin(GL_POLYGON)
    if direction : 
        glVertex(50 , 0)
        glVertex(50 + width, height)
        glVertex(50 + width, height)
        glVertex(50 , 0)
    else :
        glVertex(50, WINDOW_HEIGHT)
        glVertex(50 + width,WINDOW_HEIGHT-height)
        glVertex(50 + width, WINDOW_HEIGHT-height)
        glVertex(50 , WINDOW_HEIGHT)
    glEnd()

def circle(radius , x_c , y_c , steps = 100):
    glBegin(GL_POLYGON)    
    dtheta = 2*pi / steps 
    theta = 0 
    while theta <= 2*pi : 
        x = int (x_c + radius * cos(theta))
        y = int (y_c + radius * sin(theta)) 
        theta += dtheta 
        glVertex2i(x,y)
    glEnd()


def initialize_world():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glClearColor(0,0,0,0)
    glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)

def play():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(0.5,0,0.5)
    # pipe(128,128,1,100,100)
    pipe(409,409,1)
    glutSwapBuffers() 
    
def main(): 
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(WINDOW_WIDTH,WINDOW_HEIGHT)
    glutCreateWindow("Lab 3 B")
    initialize_world()
    glutDisplayFunc(play)
    glutIdleFunc(play)
    glutMainLoop()
if __name__ == '__main__':
    main()

