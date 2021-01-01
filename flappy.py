import pygame,sys,random,time
from pygame.locals import *
import numpy as np

### The orgin is in the upper leftt corner
### All measurements are in pixels
### 1 CM = 37.8 PIXELS

pygame.init()

WIDTH       = 1280
HEIGHT      = 720
DISPLAYSURF = pygame.display.set_mode((WIDTH,HEIGHT), pygame.FULLSCREEN)


pygame.display.flip()
pygame.display.set_caption('Dodge Game')

FPS      = 30
fpsClock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255,255,255)
RED   = (255,  0,  0)
GREEN = (  0,255,  0)
BLUE  = (  0,  0,255)
COLOR = (222,222,237)

DISPLAYSURF.fill(WHITE)

background          = pygame.image.load('bg.png').convert_alpha()
background          = pygame.transform.scale(background, (WIDTH*10,HEIGHT))
background_position = np.array([0,0])
background_velocity = np.array([0,0])
bg_x                = background_position[0]+background_velocity[0]
bg_y                = background_position[1]+background_velocity[1]


bird_position   = np.array([550,350])
gravity_vector  = np.array([0,0])  
force_vector    = np.array([0,0])
motion_x        = bird_position[0]+force_vector[0]+gravity_vector[0]
motion_y        = bird_position[1]+force_vector[1]+gravity_vector[1]

column_vertices  = np.matrix('200 400; 200 450; 205 450; 205 720; 370 720; 370 450; 375 450; 375 400')
column_vertices  = column_vertices + np.array([1100,0])
column_vertices2 = np.matrix('200 400; 200 450; 205 450; 205 720; 370 720; 370 450; 375 450; 375 400')
column_vertices2 = column_vertices2 + np.array([1750,0])
column_change    = np.random.choice([random.uniform(.6,.9),random.uniform(1.2,1.3)])
column_change2   = np.random.choice([random.uniform(.6,.9),random.uniform(1.2,1.3)])
column_velocity  = np.array([10,0])

bird_0    = pygame.image.load('bird_0.gif').convert_alpha()
bird_1    = pygame.image.load('bird_1.gif').convert_alpha()
bird_0    = pygame.transform.scale(bird_0,(70,70))
bird_1    = pygame.transform.scale(bird_1,(70,70))
animation = [bird_0]*6 + [bird_1]*6
frame_num = 0

    
def backgrounds():
    global bg_x,bg_y
    DISPLAYSURF.blit(background,(bg_x,bg_y))
    background_velocity[0] = background_velocity[0] - 5
    bg_x                   = background_position[0]+background_velocity[0]
    bg_y                   = background_position[1]+background_velocity[1]

def bird():
    global frame_num
    DISPLAYSURF.blit(animation[frame_num],(motion_x,motion_y))
    frame_num = (frame_num + 1) % len(animation)

def drawColumns():
    global column_vertices,pointlist

    frame_points_0  = (column_vertices[0:4]-2).tolist()
    frame_points_1  = (column_vertices[4:]+1).tolist()
    pointlist = column_vertices.tolist()
    pygame.draw.polygon(DISPLAYSURF,BLACK, frame_points_0+frame_points_1,3)
    pygame.draw.polygon(DISPLAYSURF,GREEN, pointlist)
    pygame.draw.line(DISPLAYSURF,BLACK, pointlist[2],pointlist[5],2)
    pygame.draw.line(DISPLAYSURF,BLACK, pointlist[0],pointlist[-1],7)


def drawColumns2():
    global column_vertices
    
    frame_points_0  = (column_vertices2[0:4]-2).tolist()
    frame_points_1  = (column_vertices2[4:]+1).tolist()
    pointlist = column_vertices2.tolist()
    pygame.draw.polygon(DISPLAYSURF,BLACK, frame_points_0+frame_points_1,3)
    pygame.draw.polygon(DISPLAYSURF,GREEN, pointlist)
    pygame.draw.line(DISPLAYSURF,BLACK, pointlist[2],pointlist[5],2)
    pygame.draw.line(DISPLAYSURF,BLACK, pointlist[0],pointlist[-1],7)
        
    
def column_height():
    global column_vertices,column_vertices2,column_change
    scaling_mat = np.matrix([[1,0],[0,column_change]])
    a = (np.vstack((column_vertices[0:3],column_vertices[5:])))*scaling_mat
    column_vertices  = np.vstack((a[0:3],column_vertices[3:5],a[3:]))
    choice = np.random.randint(0,2)
    column_change = [np.random.uniform(1.1,1.2),np.random.uniform(.8,.9)]
    column_change = column_change[choice]


def column_height2():
    global column_vertices,column_vertices2,column_change2
    scaling_mat = np.matrix([[1,0],[0,column_change2]])
    a = (np.vstack((column_vertices2[0:3],column_vertices2[5:])))*scaling_mat
    column_vertices2  = np.vstack((a[0:3],column_vertices2[3:5],a[3:]))
    choice = np.random.randint(0,2)
    column_change2 = [np.random.uniform(1.1,1.2),np.random.uniform(.8,.9)]
    column_change2 = column_change2[choice]
    
    
def column_movement():
    global column_velocity,column_vertices
    column_vertices -=  column_velocity
    if column_vertices[7,0] < 0:
        column_height()
        column_vertices = column_vertices + np.array([1300,0])


def column_movement2():
    global column_velocity,column_vertices2
    column_vertices2 -=  column_velocity
    if column_vertices2[7,0] < 0:
        column_vertices2 = column_vertices2 + np.array([1300,0])
        column_height2()
    

def control():  # the control and borders of the bird's motion
        global motion_x,motion_y
     
        if motion_y < 0:
                bird_position[1]  = 0
                force_vector[1]   = 0
                gravity_vector[1] = 0
        elif motion_y > 720:
                bird_position[1] = 720
                force_vector[1]  = 0
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[K_UP]:
                force_vector[1] -= 15

        motion_x        = bird_position[0]+force_vector[0]+gravity_vector[0]
        motion_y        = bird_position[1]+force_vector[1]+gravity_vector[1]


def gravity():
    global motion_x,motion_y
    gravity_vector[1] = gravity_vector[1] + 5 

def lose():
    global pointlist,motion_y,motion_x
    
    
    for i in range(0,8):
        
        if (pointlist[0][1] <= motion_y+45 <= pointlist[3][1]) and (pointlist[0][0] <= motion_x+45 <= pointlist[7][0]):
            time.sleep(1)
            pygame.quit()
            sys.exit()


def run_game():
    global pointlist
    while True: # main loop
        for event in pygame.event.get():
            if event.type == QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()

        backgrounds()
        control()
        gravity()
        control()
        bird()
        drawColumns()
        drawColumns2()
        column_movement()
        column_movement2()
        lose()
        
        
        pygame.display.update()
        fpsClock.tick(FPS)

run_game()
