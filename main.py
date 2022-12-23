# Outsource imports
import pygame
import math
from random import randint, choice

# Local imports
import constants
import DashboardButton
from RoadUsers import PlayerSprite
from utils import *

pygame.init()
pygame.font.init()

clock = pygame.time.Clock()

score = 0

path = []

#-------------------------------------------------------------
# Class for all borders in the scene (sidewalk, island, lane)
class Border(pygame.sprite.Sprite):
    
    def __init__(self ,type ,x ,y ,width ,height):
        # Call the parent class's constructor
        super().__init__()
        
        self.type = type

        # Make a border, of the type and size specified in the parameters
        self.image = pygame.Surface([width,height])
        
        # (x,y) == top_left of rect
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        if type == 'sidewalk':
            self.image.fill(constants.RED)
        elif type == 'island':
            self.image.fill(constants.WHITE)
        elif type == 'lane':
            self.image.fill(constants.GREEN)

#-------------------------------------------------------------

def draw(win, player_car):
    
    for img, pos in constants.LEVEL_IMGS:
        # Draw this img in this position
        win.blit(img, pos)  
    
    constants.draw_street_names()

    player_car.draw(win)

    #draw_points(path, win)
    #draw_scene_borders(win)

    pygame.draw.rect(constants.WIN, constants.GRAY, constants.DASHBOARD_RECT_HOR)
    pygame.draw.rect(constants.WIN, constants.GRAY, constants.DASHBOARD_RECT_VER)
    
    for img, pos in constants.DASH_IMGS:
        # Draw this img in this position
        win.blit(img, pos)

    draw_dashboard_texts(win)

def draw_dashboard_texts(win):
    
    countdown_text = constants.SMALL_FONT.render(f"00:00:00", 1, constants.RED)
    #win.blit(countdown_text, (WIDTH/2-120,30))

    level_text = constants.SMALL_FONT.render(f"Level 1", 1, constants.RED)
    #win.blit(level_text, (860, 60))

    # round to the first significant digit, units are px/sec
    velocity_text = constants.SMALL_FONT.render(f"{round(round(player.vel,1)*10.0)}", 1, (255, 255, 255))
    velocity_text_pos = (constants.SPEEDOMETER_TEXT_POS[0]-velocity_text.get_rect().centerx,constants.SPEEDOMETER_TEXT_POS[1]-velocity_text.get_rect().centery)
    win.blit(velocity_text, velocity_text_pos)

#--------------------------------------------------------------
def move_player(player_car):
    keys = pygame.key.get_pressed()
    gas_pressed = False
    forward_motion = False

    # Car is only able to rotate while driving forward or backward
    def rotate_player(forward_motion):
        if forward_motion:
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                player_car.rotate(left = True)
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                player_car.rotate(right = True)
        else:
            # Rotating in reverse is reversed - left is right, right is left
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                player_car.rotate(right = True)
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                player_car.rotate(left = True)


    if keys[pygame.K_w] or keys[pygame.K_UP]:
        gas_pressed = True 
        forward_motion = True
        player_car.move_forward()
        rotate_player(forward_motion)

    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        gas_pressed = True 
        player_car.move_backward()
        rotate_player(forward_motion)

    if not gas_pressed:
        player_car.reduce_speed()

#--------------------------------------------------------------
# Function for drawing path points
def draw_points(path, win):
    for point in path:
        # Draw a red point of radius 5 in the path
        pygame.draw.circle(win, constants.RED, point, 5)

def draw_scene_borders(win):
    sidewalk_borders = [(("Top_Hori_Sidewalk"), (0, 185), (constants.SCENE.get_width(), 5)),
                        (("Bot_Hori_Sidewalk_Left"), (0, 380), (243, 5)),
                        (("Bot_Hori_Sidewalk_Right"), (437, 380), (constants.SCENE.get_width()-437, 5)),
                        (("Vert_Sidewalk_Left"), (constants.SCENE.get_width()-440, 380), (5, constants.HEIGHT)),
                        (("Vert_Sidewalk_Right"), (437, 380), (5, constants.HEIGHT))]


    lane_borders = [(("Hori_Lane"), (0, 285), (constants.SCENE.get_width(), 5)),
                    (("Vert_Lane"), ((int(constants.SCENE.get_width()/2)), 285), (5, constants.HEIGHT))]

    island_borders = [(("Left_Island"), (135,273), (218-135,298-273)),
                    (("Bot_Island"), (300,381), (380-300,463-381))]

    for kind, top_left, bottom_right in sidewalk_borders:
        # Draw this kind in this position
        pygame.draw.rect(win, constants.GREEN, (*top_left, *bottom_right))
    
    for kind, top_left, bottom_right in lane_borders:
        # Draw this kind in this position
        pygame.draw.rect(win, constants.BLUE, (*top_left, *bottom_right))

    for kind, top_left, bottom_right in island_borders:
        # Draw this kind in this position
        pygame.draw.rect(win, constants.RED, (*top_left, *bottom_right))
    
    
def create_scene_borders(borders_list, all_sprite_list):

    """
    top_hori_sidewalk = Border('sidewalk',0, 185, SCENE.get_width(), 5)
    borders_list.add(top_hori_sidewalk)
    all_sprite_list.add(top_hori_sidewalk)

    bot_hori_sidewalk_left = Border('sidewalk',0, 380, 243, 5)
    borders_list.add(bot_hori_sidewalk_left)
    all_sprite_list.add(bot_hori_sidewalk_left)    
    """

    hori_lane = Border('lane', 0, 285, constants.SCENE.get_width(), 5)
    borders_list.add(hori_lane)
    all_sprite_list.add(hori_lane) 

    vert_lane = Border('lane', int(constants.SCENE.get_width()/2), 285, 5, constants.HEIGHT)
    borders_list.add(vert_lane)
    all_sprite_list.add(vert_lane) 

def handle_collision_with_borders():

    # Did the player moving caused collision with a border?
    borders_hit_list = pygame.sprite.spritecollide(player.sprite,borders_list,False)

    print(borders_hit_list)
#-------------------------------------------------------------

# Groups
player = PlayerSprite((constants.RIGHT_ROUNDABOUT_CENTER[0],constants.LEFT_ROUNDABOUT_CENTER[1]+2.5*constants.LANE_W))
playerGroup = pygame.sprite.GroupSingle()
playerGroup.add(player)

buttons_list = DashboardButton.create_buttons_list()
buttons_group = pygame.sprite.Group()
buttons_group.add(buttons_list)

borders_list = pygame.sprite.Group()
other_cars_list = pygame.sprite.Group()
other_cars_list.add(player)

#player_car = PlayerCar(5,3)

create_scene_borders(borders_list, playerGroup)
#-------------------------------------------------------------------------
running = True
# Game Loop
while running:
    # Limit our window to this max speed
    clock.tick(constants.FPS)   

    #draw(WIN, images, player_car)
    draw(constants.WIN,player)
    
    buttons_group.draw(constants.WIN)
    
    #constants.draw_screen_positions()
    constants.draw_borders()
    
    #pygame.draw.rect(WIN, GREEN, (0,0,850,490))
    #all_sprite_list.draw(WIN)

    for event in pygame.event.get():
        # If player clicked X on the window
        if event.type == pygame.QUIT:   
            running = False
            break 
        # If player clicked with left mouse button 
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get current mouse position
            m_x, m_y = pygame.mouse.get_pos()
            # Check if one of the dashboard buttons was pressed
            for button in buttons_list:
                dis = math.sqrt((button.rect.centerx-m_x)**2 + (button.rect.centery-m_y)**2)
                #pygame.draw.circle(WIN, RED, (button.rect.centerx, button.rect.centery), RADIUS)
                if (dis < constants.RADIUS):
                    button.button_pressed()

        """
        # Create the path for computer car
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            path.append(pos)
        """

    #move_player(player_car)
    move_player(player)
    
    #handle_collision_with_mask(player_car)
    #handle_collision_with_borders()

    # Update the window with everything we have drawn
    pygame.display.update()

#print(path)
#print(score)

#print(*pygame.font.get_fonts(), sep = "\n")

pygame.quit()   # Close the game cleanly