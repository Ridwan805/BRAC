from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

speed = 0.5
rain_angle_direction = 0.0
rain_drop_arr = []
bg_color = [0.09,0.09,0.09,0]
change_rate = 0.01
# house_color = [0.94,0.94, 0.74]
house_color = [0.52,0.52,0.52]

light_blue = [0.5, 0.5, 1]
white_or_blue = [1, 1, 1]


for droplets in range(250):
    r = random.randint(20, 35)
    x= random.uniform(0, 800) #randomly choosing a value of x
    y= random.uniform(0, 800) ##randomly choosing a value of y

    rain_drop_arr.append((x, y)) #top point of rain droplets 
    rain_drop_arr.append((x,y-r)) #bottom point of rain droplets

def draw_house():
    #house
    glBegin(GL_LINES)
    glColor3f(*house_color)

    glVertex2f(150,0)
    glVertex2f(150,300)

    glVertex2f(150,300)
    glVertex2f(650,300)

    glVertex2f(650,300)
    glVertex2f(650,0)

    glVertex2f(650,0)
    glVertex2f(150,0)

    for i in range(1,300):
        glVertex2f(150,i)
        glVertex2f(650,i)
    glEnd()

    #roof
    glBegin(GL_TRIANGLES)
    glColor3f(0.5, 0.2, 0.0)   
    glVertex2f(150, 300)  
    glVertex2f(650, 300)  
    glVertex2f(400,425)  
    glEnd()
    
    #door
    glBegin(GL_LINES)
    glColor3f(0, 0, 0)

    glVertex2f(350, 0)    
    glVertex2f(450, 0)

    glVertex2f(450, 0)
    glVertex2f(450, 130)
     
    glVertex2f(450, 130) 
    glVertex2f(350, 130)
    

    glVertex2f(350, 130)
    glVertex2f(350, 0)
    for i in range(1,130):
        glVertex2f(350,i)
        glVertex2f(450,i)

    glEnd()

    #inner door
    glBegin(GL_LINES)
    glColor3f(1, 1, 1) 
    
    glVertex2f(355, 5)
    glVertex2f(355, 125)

    glVertex2f(355,125)
    glVertex2f(445,125)

    glVertex2f(445,125)
    glVertex2f(445,5)

    glVertex2f(445,5)
    glVertex2f(355,5)

    for i in range(6,125):
        glVertex2f(355,i)
        glVertex2f(445,i)
    glEnd()

def draw_line(a, b, c, d):
    glLineWidth(2)  # Adjust thickness
    if bg_color == [0.09,0.09,0.09,0]:
        if random.randint(0,1) == 1:
            glBegin(GL_LINES)
            glColor3f(*light_blue )  # Light blue color
            glVertex2f(a, b)  
            glVertex2f(c, d)  
            glEnd()
        
        else:
            glBegin(GL_LINES)
            glColor3f(*white_or_blue)  # white
            glVertex2f(a, b)  
            glVertex2f(c, d)  
            glEnd()
    
    else:
        if random.randint(0,1) == 1:
            glBegin(GL_LINES)
            glColor3f(*light_blue )  # Light blue color
            glVertex2f(a, b)  
            glVertex2f(c, d)  
            glEnd()
        
        else:
            glBegin(GL_LINES)
            glColor3f(*white_or_blue)
            glVertex2f(a, b)  
            glVertex2f(c, d)  
            glEnd()

def dropping_rains():
    global rain_drop_arr

    
    for droplets in range(0, len(rain_drop_arr), 2):
        x0, y0 = rain_drop_arr[droplets]
        x1, y1 = rain_drop_arr[droplets + 1]

        #making the rain line falls downwards
        y0 -= speed
        y1 -= speed 

        if y1 < 0: #when the rain is going out of the window
            y0 = random.uniform(800, 900)  # new points creating on the top of the screen 
            y1 = y0 - random.randint(20, 35)
            x0 = random.uniform(0, 800)  # randomly getting new values of x
            x1 = x0 + rain_angle_direction  

        
        x0 += rain_angle_direction * 0.05 # multiply with something low so that the rain direction is going l or r according to use
        x1 = x0 + rain_angle_direction # bending
        
     

        # resetting x values if raindrop goes out of screen on left or right side
        if x1 < 0:  # Left side
            x0 = random.uniform(800, 900)
            x1 = x0 + rain_angle_direction
        elif x1 > 800:  # Right side
            x0 = random.uniform(-100, 0)
            x1 = x0 + rain_angle_direction

        rain_drop_arr[droplets] = (x0, y0)
        rain_drop_arr[droplets + 1] = (x1, y1)
        glutPostRedisplay()

def changing_rain_direction(key, a, b):
    global rain_angle_direction, speed

    previous_angle = rain_angle_direction
    previous_speed = speed

    if key == GLUT_KEY_LEFT:
        rain_angle_direction -= 0.75
        if speed >= 0.8:
            speed -= 0.25 #if the targetted speed is reached then the speed will reduce
        else:
            speed += 0.25 #if the targetted speed is  not reached then the speed will increase
        
        
    if key == GLUT_KEY_RIGHT:
        rain_angle_direction += 0.75
        if speed >= 0.8:
            speed -= 0.25
        else:
            speed += 0.25
         
    if abs(rain_angle_direction) >= 25: #fixing this so that the rain doesn't fall horizontally
        rain_angle_direction = previous_angle
    if speed >= 1: # fixing this so that the speed doesnt get too much 
        speed = previous_speed
    glutPostRedisplay()

def Day_to_night_tansition(key, a, b):
    global bg_color, house_color, white_or_blue
    if key == b'n':  
        bg_color = [(bg_color[0] - change_rate)]*3+ [0] #slowly decreasing the value of background for transition to night

        # the color of house is also changing with the transition 
        house_color[0] -= 0.02
        house_color[1] -= 0.02
        house_color[2] -= 0.01

        #the color of the rain
        white_or_blue[0] += 0.25
        white_or_blue[1] += 0.2
        white_or_blue[2] += .15

        if bg_color[0] < 0.09:
            bg_color = [0.09,0.09,0.09,0]

        if house_color[0] < 0.52:
            house_color = [0.52,0.52,0.52]
        
        if white_or_blue[0] > 1:
            white_or_blue = [1,1,1]
        
    elif key == b'd': 
        bg_color = [(bg_color[0] + change_rate)]*3 + [0] #slowly increasing the value of background for transition to day

        house_color[0] += 0.02
        house_color[1] += 0.02
        house_color[2] += 0.01
# blue = [0,0.2,0.35]
        white_or_blue[0] -= 0.25
        white_or_blue[1] -= 0.2
        white_or_blue[2] -= .15

        if bg_color[0] > 0.81:
            bg_color = [0.81,0.81,0.81,0]
        
        if house_color[0] > 0.94:
            house_color = [0.94,0.94,0.74]

        if white_or_blue[2] < 0.4:
            white_or_blue = [0,0.2,0.4]
    glutPostRedisplay()

def iterate():
    glViewport(0, 0, 800, 800)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 800, 0.0, 800, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def show_elements():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(*bg_color);	#//color black
    glLoadIdentity()
    iterate()
    glColor3f(0, 0, 0.1)
    draw_house()
    for i in range(0, len(rain_drop_arr), 2):
        draw_line(*rain_drop_arr[i], *rain_drop_arr[i + 1])   
    glutSwapBuffers()

glutInit() #initializing GLUT 

glutInitWindowSize(800, 800) #window size
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB) 
wind_name = glutCreateWindow(b"CSE423 Lab 1: Task 1 Building a house in rainfall") #window name

glutDisplayFunc(show_elements)
glutIdleFunc(dropping_rains)
glutSpecialFunc(changing_rain_direction)
glutKeyboardFunc(Day_to_night_tansition)

glutMainLoop()