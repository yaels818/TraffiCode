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
level = 1

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

    #for img, pos in constants.FINISH_LINE_IMGS:
    #    win.blit(img, pos)

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
    
    timer_text = constants.DASH_FONT.render(f"00:00:00", 1, constants.BLACK)
    timer_text_pos = (constants.MIRROR_CENTER-timer_text.get_rect().centerx,constants.MIRROR_POS[1]+timer_text.get_rect().centery)
    win.blit(timer_text, timer_text_pos)

    level_text = constants.CLIP_FONT.render(f"Level {level}", 1, constants.BLACK)
    level_text_pos = (constants.CLIP_LEFT+0.5*level_text.get_rect().centerx,constants.CLIP_TOP+level_text.get_rect().centery)
    win.blit(level_text, level_text_pos)

    score_text = constants.CLIP_FONT.render(f"Score: {score}", 1, constants.RED)
    score_text_pos = (constants.CLIP_CENTER-score_text.get_rect().centerx,constants.RIGHT_ROUNDABOUT_CENTER[1]-score_text.get_rect().centery)
    win.blit(score_text, score_text_pos)

    # round to the first significant digit, units are px/sec
    velocity_text = constants.DASH_FONT.render(f"{round(round(player.vel,1)*10.0)}", 1, (255, 255, 255))
    velocity_text_pos = (constants.SPEEDOMETER_TEXT_POS[0]-velocity_text.get_rect().centerx,constants.SPEEDOMETER_TEXT_POS[1]-velocity_text.get_rect().centery)
    win.blit(velocity_text, velocity_text_pos)

#--------------------------------------------------------------
def move_player(player_car):
    keys = pygame.key.get_pressed()
    gas_pressed = False
    reverse_gear = False

    if keys[pygame.K_SPACE]:
        player_car.reduce_speed(emergency_brake = True)

    if keys[pygame.K_w] or keys[pygame.K_UP]:
        gas_pressed = True 
        reverse_gear = False
        player_car.move_forward()

    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        gas_pressed = True 
        reverse_gear = True
        player_car.move_backward() 

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        if not reverse_gear:
            player_car.rotate(left = True)
        else:
            player_car.rotate(right = True)

    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        if not reverse_gear:
            player_car.rotate(right = True)
        else:
            player_car.rotate(left = True)
        
    if not gas_pressed:
        player_car.reduce_speed(emergency_brake = False)

def check_mask_collisions(player_car):
    """
    Check if player_car is colliding with any of the masks defined for this level.
    Because using masks is heavy on the CPU (due to pixel-by-pixel comparison),
    run the check on them only when the player is within their area.
    """
    global score
    player_pos = (player_car.x,player_car.y)
    relevant_mask = None

    dis_right_rbt = math.sqrt((constants.RIGHT_ROUNDABOUT_CENTER[0]-player_car.x)**2 + (constants.RIGHT_ROUNDABOUT_CENTER[1]-player_car.y)**2)
    dis_left_rbt = math.sqrt((constants.LEFT_ROUNDABOUT_CENTER[0]-player_car.x)**2 + (constants.LEFT_ROUNDABOUT_CENTER[1]-player_car.y)**2)

    if player_car.x > constants.EREZ_ROTEM_SIDEWK_TOP_R[0] and player_car.y > constants.ROTEM_ROAD_BOT_R[1]:
        # player is within right parking lot
        relevant_mask = constants.MASK_RIGHT_PL

    elif dis_right_rbt < constants.RBT_OUTER_RAD:
        # player is within right roundabout
        relevant_mask = constants.MASK_RIGHT_RBT
    
    elif dis_left_rbt < constants.RBT_OUTER_RAD:
        # player is within left roundabout
        relevant_mask = constants.MASK_LEFT_RBT

    elif player_car.x < constants.ELLA_ROAD_TOP_L[0] and player_car.y > constants.SHAKED_SIDEWK_BOT_R[1]:
        # player is within right parking lot
        relevant_mask = constants.MASK_LEFT_PL

    if relevant_mask:
        # Check if the player car is colliding any of the masks
        poi = player_car.check_collision_with_mask(relevant_mask)
        if poi != None:
            player_car.bounce()
            pygame.draw.circle(constants.WIN, constants.GREEN, poi, 2)

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

        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_q]:
                buttons_list[1].button_pressed() # left blinker
            if keys[pygame.K_e]:
                buttons_list[2].button_pressed() # right blinker

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
    
    check_mask_collisions(player)
    #handle_collision_with_mask(player_car)
    #handle_collision_with_borders()

    # Update the window with everything we have drawn
    pygame.display.update()

#print(path)
#print(score)

#print(*pygame.font.get_fonts(), sep = "\n")

pygame.quit()   # Close the game cleanly