from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
window_height = 800
window_width = 800

bg_color = [0.0, 0.0, 0.0, 0.0]
is_playing = True
is_game_over = False 
is_reset = False
score = 0
collector_movement = 0
speed = 0.07
dia_y = window_height -100
dia_x = random.uniform(25,window_width-25)
randcolor = [random.uniform(0.1,0.8),random.uniform(0.1,0.8),random.uniform(0.1,0.8)]

def zone_check(x1, y1, x2, y2):
    # checks in which zone the current point is at
    dx = x2 - x1
    dy = y2 - y1

    if abs(dx) >= abs(dy):
        if dx >= 0 and dy >= 0:
            return 0
        elif dx >= 0 and dy <= 0:
            return 7
        elif dx <= 0 and dy >= 0:
            return 3
        elif dx <= 0 and dy <= 0:
            return 4
    else:
        if dx >= 0 and dy >= 0:
            return 1
        elif dx >= 0 and dy <= 0:
            return 6
        elif dx <= 0 and dy >= 0:
            return 2
        elif dx <= 0 and dy <= 0:
            return 5

def zone_m_to_zone_zero(x1, y1, x2, y2, zone):
    #converts any other zone points to zone 0
    if zone == 0:
        return x1, y1, x2, y2
    elif zone == 1:
        return y1, x1, y2, x2
    elif zone == 2:
        return y1, -x1, y2, -x2
    elif zone == 3:
        return -x1, y1, -x2, y2
    elif zone == 4:
        return -x1, -y1, -x2, -y2
    elif zone == 5:
        return -y1, -x1, -y2, -x2
    elif zone == 6:
        return -y1, x1, -y2, x2
    elif zone == 7:
        return x1, -y1, x2, -y2
    
def zone_zero_to_zone_m(x,y,zone): 
    #coverts the zone 0 to its original zone
    if zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y
    elif zone == 0:
        return x, y

def midpoint_line(x1, y1, x2, y2):   
    zone = zone_check(x1, y1, x2, y2) #finds the zone 
    x1, y1, x2, y2 = zone_m_to_zone_zero(x1, y1, x2, y2, zone)#convert the zone to zone 0
    
    dx = x2 - x1
    dy = y2 - y1
    d = (2 * dy) - dx
    incE = 2 * dy #East
    incNE = 2 * (dy - dx) #North East
    x, y = x1, y1
    glPointSize(3)
    glBegin(GL_POINTS)
    while x <= x2:  #X2 always increases
        conX, conY = zone_zero_to_zone_m(x, y, zone) #converts back the zone to original zone 
        
        glVertex2f(conX, conY)
        if d >= 0: # pixel moves to north east
            d += incNE
            y += 1
        else: # pixel moves to east
            d += incE
        x += 1
    glEnd()

def draw_quit(a, b):
    glColor3f(1,0,0)
    midpoint_line(a-15, b-15, a+15, b+15)
    midpoint_line(a-15, b +15, a+15, b-15)

def draw_back(a, b):
    glColor3f(0,0,1)
    midpoint_line(a+25, b, a-15, b) #horizontal line
    midpoint_line(a+5, b+15, a-15, b) # upper
    midpoint_line(a+5, b-15, a-15, b) # lower

def draw_pause_play(a, b):
    if is_playing == True: #unpause
        glColor3f(0.0, 1.0, 0.0)
        midpoint_line(a-10, b+15,a-10, b-15)
        midpoint_line(a+10, b+15,a+10, b-15)
        
    else: #pause
        glColor3f(1.0, 0.75, 0.0)
        midpoint_line(a - 10, b + 15, a - 10, b - 15)
        midpoint_line(a - 10, b + 15, a + 10, b) #up
        midpoint_line(a - 10, b - 15, a + 10, b) #below

def draw_buttons():
    draw_quit(window_width-50, window_height-50)
    draw_back(50, window_height-50)
    draw_pause_play(window_width// 2, window_height-50)

def game_start():
    global dia_x, dia_y, score, is_game_over, is_playing, collector_movement, speed, randcolor
    
    #for collector 
    if is_game_over == False: #if the game is over 
        glColor3f(1,1,1)#red
    else: #if the game is runing 
        glColor(1,0,0) #white
    midpoint_line((window_width//2)-75 +collector_movement, 0, (window_width//2)+75+collector_movement, 0) #base 
    
    midpoint_line((window_width//2)-100+collector_movement, 25, (window_width//2)+100+collector_movement, 25 )# upper
    
    midpoint_line((window_width//2)-75+collector_movement, 0, (window_width//2)-100+collector_movement, 25) #left
    
    midpoint_line((window_width//2)+75+collector_movement, 0, (window_width//2)+100+collector_movement, 25) #right

    #for diamond
    glColor3f(*randcolor)
    
    midpoint_line(dia_x,dia_y, dia_x+15,dia_y-20) #top to right
    
    midpoint_line(dia_x+15,dia_y-20,dia_x ,dia_y-40) #right to bottom
    
    midpoint_line(dia_x, dia_y-40, dia_x-15, dia_y-20) #bottom to left 
    
    midpoint_line(dia_x-15, dia_y-20, dia_x, dia_y) #left to top
    
    if is_playing == False: # Codition happens then pause
        return  

    dia_y -= speed #makes the diamond fall 
    
    if dia_y - 40 <= 25 and ((window_width//2)-100+ collector_movement) <= dia_x <= ((window_width//2)+100 + collector_movement):  #when the diamond is caught in the collector 
            
            score += 1  
            print("Score:", score)
            
            dia_y = window_height - 100  # reset diamond position from above
            dia_x = random.uniform(25, 775) #random x place
            randcolor = [random.uniform(0.1,0.8),random.uniform(0.1,0.8),random.uniform(0.1,0.8)]
            
    elif dia_y - 40 <= -40 :  # when the diamond is not caught in the collector 
            if not is_game_over:  
                print("GAME OVER! Final Score:", score)
            is_game_over = True  #the game is over 

              
    #increase speed after a interval of score
    if score == 5:
        speed = 0.09
    elif score == 10:
        speed = 0.13
    elif score == 13:
        speed = 0.17
        

    
    glutPostRedisplay()

def left_right_movement(key,x,y):
    global collector_movement, is_game_over, is_playing, score
    if is_game_over or not is_playing: #if game is paused or end everything should be where it is 
        return
    
    if key == GLUT_KEY_LEFT:
        if collector_movement > -294:  # Prevent moving too far left
            collector_movement -=8
            
    elif key == GLUT_KEY_RIGHT:
        if collector_movement < 294:  # Prevent moving too far right
            collector_movement +=8
    glutPostRedisplay() 

def buttons_function(button, state,x,y):
    global is_playing, score, is_reset, collector_movement, dia_x,dia_y, speed, is_game_over
    y = 800 - y 
    
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if ((window_width//2)-10)<= x <=((window_width//2)+10) and (window_height-50  -15) <= y <= (window_height-50 +15): #when pause/resume is pressed
            is_playing = not is_playing
            
        
        if (window_width-50-15)<= x <=(window_width-50+15) and (window_height-50 -15) <= y <= (window_height-50 +15): #when quit is pressed 
            glutLeaveMainLoop() 
        
        if (35) < x < (75) and (window_height-50 -15) <= y <= (window_height-50 +15): #when restart is pressed 
            is_reset = True
            is_playing = True #making sure that the game is not paused 
            is_game_over = False #if the game is over making sure that the game is not over 
            print('Starting Over!!')
            #initializing all to starting values
            score = 0
            speed = 0.07
            collector_movement = 0
            dia_y = window_height -100
            dia_x = random.uniform(25,window_width-25)  
           
    glutPostRedisplay()

def iterate():
    glViewport(0, 0, window_width, window_height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, window_width, 0.0, window_height, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def start():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(*bg_color)
    glLoadIdentity()
    iterate()
    draw_buttons()
    
    game_start()
    glutSwapBuffers()


glutInit()
glutInitWindowSize(800, 800) #window size
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB) 
wind = glutCreateWindow(b"CSE423 Lab 2") #window name
glutDisplayFunc(start)
glutMouseFunc(buttons_function)
glutSpecialFunc(left_right_movement)
glutIdleFunc(game_start)
glutMainLoop()