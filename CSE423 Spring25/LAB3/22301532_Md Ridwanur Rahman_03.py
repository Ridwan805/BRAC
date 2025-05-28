from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
from math import *

# Camera-related variables
last_camera_coords = None #for the gun view 
camera_pos = (0,500,500) #initial camera position
first_person_mode = False
cheat_mode = False  
gun_follow_mode = False

fovY = 120  # Field of view
GRID_LENGTH = 600  # Length of grid lines
rand_var = 423

game_over = False  
life_remaining = 5
score = 0
bullets_missed = 0

player_pos = [0, 0, 0]
player_angle = 0 
player_fall_angle = 0 
player_rotate_speed = 10  
player_speed = 30  
gun_barrel_length = 80 

bullet_speed = 10 
bullet_height = 100 
bullet_pos = player_pos  
bullet_angle = player_angle  
bullets = []  # store bullet positions and angles

enemies = []  # store enemy positions
enemy_radius = 50  # radius of the enemy to check play enemy collision
enemy_speed = 0.04  # speed at which enemies move toward the player
time_elapsed = 0  # tracks the elapsed time for pulsing

def initializing_enemy():
    global enemies
    while len(enemies) < 5:
        x = random.randint(-GRID_LENGTH + 100, GRID_LENGTH - 100)
        y = random.randint(-GRID_LENGTH + 100, GRID_LENGTH - 100)
        z = 50  # Fixed height for enemies
        enemies.append({'pos': (x, y, z)})
        
def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    
    # Set up an orthographic projection that matches window coordinates
    gluOrtho2D(0, 1000, 0, 800)  # left, right, bottom, top
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Draw text at (x, y) in screen coordinates
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    
    # Restore original projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_shapes():
    if not game_over:
        draw_player()
    else:
        draw_player()
        draw_enemies()
        draw_bullets()

def draw_player():
    global player_pos, player_fall_angle, game_over, player_angle

    glPushMatrix()  # Save the current matrix state

    x, y, z = player_pos  # unpack player position
    glTranslatef(x, y, z)  # move to the position of the player
    glRotatef(180, 0, 0, 1)  # rotate to 180 degree along the z axis 
    glRotatef(player_angle, 0, 0, 1)  # rotates to the player direction
    if game_over:
        glRotatef(player_fall_angle, 0, 1, 0) # if the game is over the player falls with respect to y axis
    
    # player body
    glColor3f(0, 0.4, 0)
    glTranslatef(0, 0, 100)  
    glScalef(0.5, 1, 2)  # Scale the cube to make it a cuboid (2x width, 1x height, 1x depth)
    glutSolidCube(50) # Take cube size as the parameter
    glScalef(2, 1, 0.5)
    glTranslatef(0, 0, -100)
    
    # player legs
    glColor3f(0, 0, 1)
    glTranslatef(0, 10, 50)
    glRotatef(180, 0, 1, 0)  
    gluCylinder(gluNewQuadric(), 10, 5, 50, 10, 10) 
    
    # undoing to previous state 
    glRotatef(-180, 0, 1, 0)  
    glTranslatef(0, -10, -50)
    
    # second leg 
    glTranslatef(0, -10, 50)
    glRotatef(180, 0, 1, 0)  
    gluCylinder(gluNewQuadric(), 10, 5, 50, 10, 10)  
    glRotatef(-180, 0, 1, 0)  
    glTranslatef(0, 10, -50)
    
    #for the head 
    glColor3f(0, 0, 0)
    glTranslatef(0, 0, 165) 
    gluSphere(gluNewQuadric(), 15, 10, 10)  
    glTranslatef(0, 0, -165) 
    
    #the arms 
    glColor3f(1, 0.8, 0.6)  
    glTranslatef(0, 30, 125)
    glRotatef(-90, 0, 1, 0)  
    gluCylinder(gluNewQuadric(), 10, 5, 50, 10, 10)  
    
    # resetting 
    glRotatef(90, 0, 1, 0)  
    glTranslatef(0, -30, -125)
    
    #second arm
    glTranslatef(0, -30, 125)
    glRotatef(-90, 0, 1, 0)  
    gluCylinder(gluNewQuadric(), 10, 5, 50, 10, 10)  
    glRotatef(90, 0, 1, 0)  
    glTranslatef(0, 30, -125)

    # for the gun 
    glColor3f(0.5, 0.5, 0.5)  
    glTranslatef(0, 0, 125)  
    glRotatef(-90, 0, 1, 0)  
    glScalef(1, 1, 2)  
    gluCylinder(gluNewQuadric(), 10, 3, 40, 10, 10)  
    glScalef(1, 1, 0.5) 
    glRotatef(90, 0, 1, 0)
    glTranslatef(0, 0, -125)  

    glPopMatrix()  # restore the previous matrix state  
    
def draw_enemies():
    global enemies, time_elapsed, enemy_radius

    scale_factor = 1 + 0.2 * sin(time_elapsed)  # Oscillates between 0.8 and 1.2

    for enemy in enemies:
        glPushMatrix()  # Save the current matrix state

        x, y, z = enemy['pos']  
        glTranslatef(x, y, z)  
        glScalef(scale_factor, scale_factor, scale_factor)  
        glColor3f(1, 0, 0) 
        glutSolidSphere(enemy_radius, 10, 10)  
        glColor3f(0, 0, 0)  
        glTranslatef(0, 0, 75) 
        glutSolidSphere(enemy_radius//2 , 10, 10)  
        glTranslatef(0, 0, -75)
        
        glPopMatrix()  # Restore the previous matrix state

def draw_bullets():
    global bullets
    # Draw each bullet
    for bullet in bullets:
        glPushMatrix()
        glTranslatef(bullet['pos'][0], bullet['pos'][1], bullet['pos'][2])
        glRotatef(bullet['angle'], 0, 0, 1) 
        glColor3f(1, 0, 0)  
        glutSolidCube(10)  
        glPopMatrix()
        
def restart_game():
    global game_over, cheat_mode, life_remaining, score, bullets_missed
    global player_pos, player_angle, bullets, enemies, player_fall_angle, gun_follow_mode

    game_over = False
    cheat_mode = False
    gun_follow_mode = False
    life_remaining = 5
    score = 0
    bullets_missed = 0
    player_pos = [0, 0, 0]
    player_angle = 0
    bullets = []
    enemies = []
    player_fall_angle = 0
    initializing_enemy()
    print("Game restarted!")
   
def keyboardListener(key, x, y):
    global player_pos, player_angle, cheat_mode, gun_follow_mode, game_over, first_person_mode

    move_step = 10  # how far the player moves
    rot_step = 10   # how much the player rotates per key press
    if game_over:
        if key == b'r':
            restart_game()
        return
    if key == b'r':
            restart_game()
            
    if key == b'w':  # Move forward
        new_x = player_pos[0] + move_step * cos(radians(player_angle))
        new_y = player_pos[1] + move_step * sin(radians(player_angle))
        
        if -GRID_LENGTH +50 <= new_x <= GRID_LENGTH -50 :
            player_pos[0] = new_x
        if -GRID_LENGTH +50 <= new_y <= GRID_LENGTH -50:
            player_pos[1] = new_y

    elif key == b's':  # Move backward
        new_x = player_pos[0] - move_step * cos(radians(player_angle))
        new_y = player_pos[1] - move_step * sin(radians(player_angle))
        if -GRID_LENGTH + 55 <= new_x <= GRID_LENGTH - 55:
            player_pos[0] = new_x
        if -GRID_LENGTH + 55 <= new_y <= GRID_LENGTH - 55 :
            player_pos[1] = new_y

    elif key == b'a':  # Rotate left
        player_angle = (player_angle + rot_step) 

    elif key == b'd':  # Rotate right
        player_angle = (player_angle - rot_step) 

    elif key == b'r' and game_over:  # Restart game
        restart_game()

    elif key == b'c':  # Toggle cheat mode
        cheat_mode = not cheat_mode
        if not cheat_mode:
            gun_follow_mode = False
        

    elif key == b'v':  # Toggle gun-follow camera in cheat + first-person
        if cheat_mode and first_person_mode:
            gun_follow_mode = not gun_follow_mode
            

    glutPostRedisplay()
    
def specialKeyListener(key, x, y):
    global camera_pos, first_person_mode

    if not first_person_mode:
        x, y, z = camera_pos

        if key == GLUT_KEY_LEFT:
            angle = -5
            x_new = x * cos(radians(angle)) - y * sin(radians(angle))
            y_new = x * sin(radians(angle)) + y * cos(radians(angle))
            camera_pos = (x_new, y_new, z)

        elif key == GLUT_KEY_RIGHT:
            angle = 5
            x_new = x * cos(radians(angle)) - y * sin(radians(angle))
            y_new = x * sin(radians(angle)) + y * cos(radians(angle))
            camera_pos = (x_new, y_new, z)

        elif key == GLUT_KEY_UP:
            z += 10
            camera_pos = (x, y, z)

        elif key == GLUT_KEY_DOWN:
            z -= 10
            camera_pos = (x, y, z)

        print(f"Camera Pos: {camera_pos}")

def mouseListener(button, state, x, y):
    global bullets, first_person_mode, gun_follow_mode, player_pos, player_angle, bullet_height, gun_barrel_length

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        angle_rad = radians(player_angle)
        bullet_x = player_pos[0] + gun_barrel_length * cos(angle_rad)
        bullet_y = player_pos[1] + gun_barrel_length * sin(angle_rad)
        bullet_z = bullet_height

        bullet = {
            "pos": [bullet_x, bullet_y, bullet_z],
            "angle": player_angle
        }
        bullets.append(bullet)

    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN: #first person and third person
        first_person_mode = not first_person_mode 
        gun_follow_mode = False  # reset follow mode when switching
        print(f"Camera mode set to: {'First-person' if first_person_mode else 'Third-person'}")

def setupCamera():
    
    global first_person_mode, player_pos, player_angle, gun_follow_mode, cheat_mode, camera_pos, last_camera_coords
    glMatrixMode(GL_PROJECTION)  
    glLoadIdentity() 
    
    gluPerspective(fovY, 1.25, 0.1, 1500) 
    glMatrixMode(GL_MODELVIEW) 
    glLoadIdentity()  

    if first_person_mode: 
        head_offset = 200  
        shoulder_offset = -25
        backward_offset = 75 
        x, y, z = player_pos

        # Calculate the right direction vector based on the player's angle
        right_x = -sin(radians(player_angle)) * shoulder_offset
        right_y = cos(radians(player_angle)) * shoulder_offset

        # Calculate the backward direction vector based on the player's angle
        backward_x = -cos(radians(player_angle)) * backward_offset
        backward_y = -sin(radians(player_angle)) * backward_offset

        camera_x = x + gun_barrel_length * cos(radians(player_angle)) * 0.25 + right_x + backward_x
        camera_y = y + gun_barrel_length * sin(radians(player_angle)) * 0.25 + right_y + backward_y
        camera_z = z + head_offset
        
    
        # when v is press or if gun_follow_mode is active
        if first_person_mode and gun_follow_mode:
            gluLookAt(last_camera_coords[0], last_camera_coords[1], last_camera_coords[2],  # Camera position
                    last_camera_coords[3], last_camera_coords[4], last_camera_coords[5],  # Look-at target
                    0, 0, 1)
        else:
            look_at_x = camera_x + cos(radians(player_angle))
            look_at_y = camera_y + sin(radians(player_angle))
            last_camera_coords = (camera_x, camera_y, camera_z, look_at_x, look_at_y, camera_z)
            gluLookAt(camera_x, camera_y, camera_z,  # Camera position
                    look_at_x, look_at_y, camera_z,  # Look-at target
                    0, 0, 1)  # Up vector (z-axis)
        
        
    else:
        
        x, y, z = camera_pos
        gluLookAt(x, y, z,  # Camera position
                  0, 0, 0,  # Look-at target
                  0, 0, 1)  # Up vector (z-axis)

def showScreen():
    global GRID_LENGTH
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
    setupCamera()
    tile_size = 80
    grid_count = GRID_LENGTH // tile_size

    # Draw grid floor
    for x in range(-grid_count, grid_count):
        for y in range(-grid_count, grid_count):
            if (x + y) % 2 == 0:
                glColor3f(0.7, 0.5, 0.95)
            else:
                glColor3f(1.0, 1.0, 1.0)

            x_start = x * tile_size
            y_start = y * tile_size

            glBegin(GL_QUADS)
            glVertex3f(x_start, y_start, 0)
            glVertex3f(x_start + tile_size, y_start, 0)
            glVertex3f(x_start + tile_size, y_start + tile_size, 0)
            glVertex3f(x_start, y_start + tile_size, 0)
            glEnd()
    # Draw boundaries
    wall_min = -GRID_LENGTH + 50
    wall_max = GRID_LENGTH -50
    wall_height = 100
    base_z = 0

    # LEFT wall (along X = wall_min)
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_QUADS)
    glVertex3f(wall_min, wall_min, base_z)
    glVertex3f(wall_min, wall_min, wall_height)
    glVertex3f(wall_min, wall_max, wall_height)
    glVertex3f(wall_min, wall_max, base_z)
    glEnd()

    # RIGHT wall (along X = wall_max)
    glColor3f(0.0, 1.0, 1.0)
    glBegin(GL_QUADS)
    glVertex3f(wall_max, wall_min, base_z)
    glVertex3f(wall_max, wall_min, wall_height)
    glVertex3f(wall_max, wall_max, wall_height)
    glVertex3f(wall_max, wall_max, base_z)
    glEnd()

    # BOTTOM wall (along Y = wall_min)
    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_QUADS)
    glVertex3f(wall_min, wall_min, base_z)
    glVertex3f(wall_max, wall_min, base_z)
    glVertex3f(wall_max, wall_min, wall_height)
    glVertex3f(wall_min, wall_min, wall_height)
    glEnd()

    # TOP wall (along Y = wall_max)
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_QUADS)
    glVertex3f(wall_min, wall_max, base_z)
    glVertex3f(wall_max, wall_max, base_z)
    glVertex3f(wall_max, wall_max, wall_height)
    glVertex3f(wall_min, wall_max, wall_height)
    glEnd()


    # Draw game elements
    
    if not game_over:
        draw_shapes()
        draw_enemies()
        draw_bullets()
    else:
        draw_player()
    

    
    if game_over:
        draw_text(10, 710, f"GAME OVER. You're score is {score}", font=GLUT_BITMAP_TIMES_ROMAN_24)
        draw_text(10, 650, "Press 'R' to RESTART THE GAME", font=GLUT_BITMAP_HELVETICA_18)
    
    else: 
        draw_text(10, 710, f"Player Life Remaining: {life_remaining}")
        draw_text(10, 650, f"Game Score: {score}")
        draw_text(10, 680, f"Player Bullet Missed: {bullets_missed}")

    glutSwapBuffers()

def idle():
    global time_elapsed, bullets, enemies, score, bullets_missed
    global game_over, life_remaining, player_fall_angle, player_angle, cheat_mode

    if game_over:
        glutPostRedisplay()
        return
    time_elapsed += 0.1

    # shoot bullet
    for bullet in bullets[:]:
        bullet['pos'][0] += bullet_speed * cos(radians(bullet['angle']))
        bullet['pos'][1] += bullet_speed * sin(radians(bullet['angle']))

        # Remove bullets that go out of bounds
        if abs(bullet['pos'][0]) > GRID_LENGTH or abs(bullet['pos'][1]) > GRID_LENGTH:
            if 'cheat' in bullet:
                is_cheat = True
            else:
                is_cheat = False
            bullets.remove(bullet)
            if not is_cheat:
                bullets_missed += 1
                if bullets_missed == 10:
                    game_over = True
                    player_fall_angle = 90

    # Move enemies toward player
    for enemy in enemies:
        dx = player_pos[0] - enemy['pos'][0]
        dy = player_pos[1] - enemy['pos'][1]
        distance = sqrt(dx**2 + dy**2)
        if distance > 1:
            enemy['pos'] = (
                enemy['pos'][0] + (dx / distance) * enemy_speed,
                enemy['pos'][1] + (dy / distance) * enemy_speed,
                enemy['pos'][2]
            )

    #enemy collision with player
    for enemy in enemies[:]:
        dx = player_pos[0] - enemy['pos'][0]
        dy = player_pos[1] - enemy['pos'][1]
        distance = sqrt(dx**2 + dy**2) 
        if distance < enemy_radius:
            if not game_over:
                life_remaining -= 1
                print(f"Life reduced! Remaining: {life_remaining}")
                if life_remaining <= 0:
                    game_over = True
                    player_fall_angle = 90 
                enemies.remove(enemy)
                initializing_enemy()
    

    # bullet enemy collisions
    for enemy in enemies[:]:
        for bullet in bullets[:]:
            dx = bullet['pos'][0] - enemy['pos'][0]
            dy = bullet['pos'][1] - enemy['pos'][1]
            if sqrt(dx**2 + dy**2) < enemy_radius:
                enemies.remove(enemy)
                bullets.remove(bullet)
                score += 10
                initializing_enemy()
                break

    # cheat mode 
    if cheat_mode and not game_over:
        # Rotate player slowly
        player_angle = player_angle + 0.6
        

        closest_enemy = None
        smallest_difference = 360  # start with max difference

        # find the enemy closest to the player's aim
        for enemy in enemies:
            dx = enemy['pos'][0] - player_pos[0]
            dy = enemy['pos'][1] - player_pos[1]
            angle_to_enemy = degrees(atan2(dy, dx)) % 360

            # get the smallest angle difference
            difference = abs((angle_to_enemy - player_angle + 180) % 360 - 180)

            if difference < smallest_difference:
                smallest_difference = difference
                closest_enemy = enemy

        #fire if the enemy line of sight is 10 degree
        if closest_enemy and smallest_difference < 10:
            already_shot = False

            # to avoid spam
            for b in bullets[-3:]:
                diff = abs((b['angle'] - player_angle + 180) % 360 - 180)
                if diff < 1:
                    already_shot = True 
                    break

            # if no similar bullet was fired recently, shoot a new one
            if not already_shot:
                bullets.append({
                    "pos": [player_pos[0], player_pos[1], bullet_height],
                    "angle": player_angle,
                    "cheat": True  # mark as cheat mode bullet
                })


    # if life is zero game over 
    if life_remaining <= 0 and not game_over:
        game_over = True
        player_fall_angle = 90
        bullets.clear() 

    glutPostRedisplay()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutCreateWindow(b"Bullet Frenzy")

    glEnable(GL_DEPTH_TEST)

    initializing_enemy()

    glutDisplayFunc(showScreen)
    glutIdleFunc(idle)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)

    glutMainLoop()

if __name__ == "__main__":
    main()