# Task 2 
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

bg_color = [0.0, 0.0, 0.0, 0.0]
frezee_frame = False # for pause 
blinking_points = False # blinking 
diagonal = [(1,1),(1,-1),(-1,1),(-1,-1)]
speed = 0.01
points_and_dir = [] #cordinates and direction of the balls 
color = [] #list for storing random color of a ball
blink_col = [] #we will store an equal length of color list but all the color will be in black
temp = None

def create_new_balls(x, y):
    X = x  
    Y = 800 - y 
    return X, Y

def pause(key,a,b):
    global frezee_frame
    if key == b' ':
        if frezee_frame == False:
            frezee_frame = True
            print('pause')
        else:
            frezee_frame = False 
            print('unpause')

def Inc_Dec_speed_key(key, a, b):
    global speed

    if key == GLUT_KEY_UP:
        speed += 0.01
        if speed > 0.3:
            speed = 0.3
            
    if key == GLUT_KEY_DOWN:
        speed -= 0.01
        if speed < 0.01:
            speed = 0.01
    
    glutPostRedisplay()

def blink_or_add_points(button, state, x, y):
    global points_and_dir, frezee_frame, blinking_points, color, temp, blink_col
    if frezee_frame == False :
        if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN and blinking_points == False: #when the blink is not happening only then
                a,b = create_new_balls(x,y)
                c =  random.choice(diagonal)
                points_and_dir.append([a,b,c])
                color.append((random.uniform(0.1, 1),random.uniform(0.1, 1),random.uniform(0.1, 1))) #a random color is intializing for the ball
                # print(f"Added point at ({a}, {b}) with direction {c}")
        
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            if blinking_points == False:  # the points/balls disappears 
                blinking_points = True
                blink_col = [(0, 0, 0)] * len(color)  # as the bg color is black so making the color of the balls full black
                temp = color  # storing the original color in the temporary
                color = blink_col  # Replace color list with black for blinking
                print('yes blink')

            else: 
                blinking_points = False #when the ball again appears 
                color = temp 
                print('No blink')
                

    glutPostRedisplay()

def move_points():
    global frezee_frame, speed, points_and_dir, diagonal, blinking_points
    glutPostRedisplay() 
    if frezee_frame is False: #when pause is not happening 
        if blinking_points == False:
            for i in range(len(points_and_dir)):
                x0,y0,c = points_and_dir[i]
                x1,y1 = c
                x0 += x1 *speed
                y0 += y1 *speed
                if x0 < 0 or x0 > 800:
                    x1 *= -1
                if y0 < 0 or y0 > 800:
                    y1 *= -1 
                points_and_dir[i] = [x0 , y0, (x1,y1)]
    
    else: 
        return
         
def iterate():
    glViewport(0, 0, 800, 800)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 800, 0.0, 800, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def MAIN():
    global color
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(*bg_color);	#//color black
    glLoadIdentity()
    iterate()
    if len(points_and_dir) > 0:
        for i in range(len(points_and_dir)):
            a,b,c = points_and_dir[i]
            glPointSize(8)
            glBegin(GL_POINTS)
            if blinking_points == True:
                glColor3f(0,0,0)
            else:
                glColor3f(*color[i])
                glVertex2f(a, b)
            glEnd()

    glutSwapBuffers()
    

glutInit()
glutInitWindowSize(800, 800) #window size
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB) 
wind = glutCreateWindow(b"CSE423 Lab 1") #window name
glutDisplayFunc(MAIN)
glutIdleFunc(move_points)
glutMouseFunc(blink_or_add_points)
glutSpecialFunc(Inc_Dec_speed_key)
glutKeyboardFunc(pause)

glutMainLoop()