# Outsource imports
import pygame
import math
from random import randint, choice
from LevelTracker import LevelTracker

# Local imports
import constants
import DashboardButton
from RoadUsers import PlayerCar
from utils import *

pygame.init()
pygame.font.init()

clock = pygame.time.Clock()

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
    
    def draw_dashboard_texts(win):

        # round to the first significant digit, units are px/sec
        velocity_text = constants.DASH_FONT.render(f"{round(round(player.vel,1)*10.0)}", 1, (255, 255, 255))
        velocity_text_pos = (constants.SPEEDOMETER_TEXT_POS[0]-velocity_text.get_rect().centerx,constants.SPEEDOMETER_TEXT_POS[1]-velocity_text.get_rect().centery)

        DASH_TEXTS = [(velocity_text, velocity_text_pos)]
        
        for txt, pos in DASH_TEXTS:
            # Draw this img in this position
            win.blit(txt, pos)  
                  
    for img, pos in constants.LEVEL_IMGS:
        # Draw this img in this position
        win.blit(img, pos)  
    
    for img, pos in constants.FINISH_LINE_IMGS:
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

    level_tracker.display()

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

def handle_collisions_with_road_borders(player_car):
    """
    
    """
    def check_mask_collisions(player_car, mask):
        """
        Check if player_car is colliding with any of the masks defined for this level.
        Because using masks is heavy on the CPU (due to pixel-by-pixel comparison),
        run the check on them only when the player is within their area.
        """
        
        # Check if the player car is colliding any of the masks
        poi = player_car.check_collision_with_mask(mask)
        if poi != None:
            player_car.bounce()
            pygame.draw.circle(constants.WIN, constants.GREEN, poi, 2)
            return True
        return False


    MID_POINT = constants.YAAR_ROAD_BOT_L[0]

    #player_car_rect = player_car.rect
    #pygame.draw.circle(constants.WIN, constants.GREEN, player_car.rect.center, 2)
    #player_car_rect.inflate_ip(-0.5,-0.5)
    #pygame.draw.rect(constants.WIN,constants.PINK, player_car_rect,4)

    # player is on the right side of the scene
    if player_car.x > MID_POINT:
        # count mask collisions
        #if player_car.x > constants.EREZ_ROTEM_SIDEWK_TOP_R[0] and player_car.y > constants.ROTEM_ROAD_BOT_R[1]:
        # check if player_car is completely inside the parking lot
        if constants.RIGHT_PL_BORDER_RECT.contains(player_car.rect):
            if check_mask_collisions(player_car, constants.MASK_RIGHT_PL):
                level_tracker.add_parking_lot_hit()
        else:
            dis_right_rbt = math.sqrt((constants.RBT_RIGHT_CENTER[0]-player_car.x)**2 + (constants.RBT_RIGHT_CENTER[1]-player_car.y)**2)
            if dis_right_rbt < constants.RBT_OUTER_RAD:
                if check_mask_collisions(player_car, constants.MASK_RIGHT_RBT):
                    level_tracker.add_roundabout_hit()
            else:
        # count regular collisions
                if player_car.rect.collidelist(constants.ROTEM_ROAD_BORDERS) != -1:
                    print("collision, ROTEM")
                    level_tracker.add_sidewalk_hit()
                elif player_car.rect.collidelist(constants.EREZ_ROAD_BORDERS) != -1:
                    print("collision, EREZ")
                    level_tracker.add_sidewalk_hit()
                elif player_car.rect.collidelist(constants.YAAR_ROAD_BORDERS) != -1:
                    print("collision, YAAR")
                    level_tracker.add_sidewalk_hit()
                        
    # player is on the left side
    else:
        # count mask collisions
        #if player_car.x < constants.ELLA_ROAD_TOP_L[0] and player_car.y > constants.SHAKED_SIDEWK_BOT_R[1]:
        # check if player_car is completely inside the parking lot
        if constants.LEFT_PL_BORDER_RECT.contains(player_car.rect):
            if check_mask_collisions(player_car, constants.MASK_LEFT_PL):
                level_tracker.add_parking_lot_hit()
        else:
            dis_left_rbt = math.sqrt((constants.RBT_LEFT_CENTER[0]-player_car.x)**2 + (constants.RBT_LEFT_CENTER[1]-player_car.y)**2)
            if dis_left_rbt < constants.RBT_OUTER_RAD:
                if check_mask_collisions(player_car, constants.MASK_LEFT_RBT):
                    level_tracker.add_roundabout_hit()
            else:
        # count regular collisions
                if player_car.rect.collidelist(constants.HADAS_ROAD_BORDERS) != -1:
                    print("collision, HADAS")
                    level_tracker.add_sidewalk_hit()
                elif player_car.rect.collidelist(constants.EREZ_ROAD_BORDERS) != -1:
                    print("collision, EREZ")
                    level_tracker.add_sidewalk_hit()
                elif player_car.rect.collidelist(constants.ELLA_ROAD_BORDERS) != -1:
                    print("collision, ELLA")
                    level_tracker.add_sidewalk_hit()
                elif player_car.rect.collidelist(constants.SHAKED_ROAD_BORDERS) != -1:
                    print("collision, SHAKED")
                    level_tracker.add_sidewalk_hit()
                elif player_car.rect.collidelist(constants.ESHEL_ROAD_BORDERS) != -1:
                    print("collision, ESHEL")
                    level_tracker.add_sidewalk_hit()


def handle_collision_with_finish_line(player_car):
    
    curr_finish_line = level_tracker.level - 1

    # get the rectangle of the finish line for this level, 
    # then move it to the right coordinates
    finish_line_rect = constants.FINISH_LINE_IMGS[curr_finish_line][0].get_rect()
    finish_line_rect.move_ip(constants.FINISH_LINE_IMGS[curr_finish_line][1])
    
    # check if player_car's center is colliding with finish_line_rect -
    # if the player crossed the finish line
    if finish_line_rect.collidepoint(player_car.rect.center):
        print("collision, Finish line")

#--------------------------------------------------------------
# Function for drawing path points
def draw_points(path, win):
    for point in path:
        # Draw a red point of radius 5 in the path
        pygame.draw.circle(win, constants.RED, point, 5)
    
def create_scene_borders(borders_list, all_sprite_list):

    """
    top_hori_sidewalk = Border('sidewalk',0, 185, SCENE.get_width(), 5)
    borders_list.add(top_hori_sidewalk)
    all_sprite_list.add(top_hori_sidewalk)

    bot_hori_sidewalk_left = Border('sidewalk',0, 380, 243, 5)
    borders_list.add(bot_hori_sidewalk_left)
    all_sprite_list.add(bot_hori_sidewalk_left)    
    """

    vert_lane = Border('lane', int(constants.SCENE.get_width()/2), 285, 5, constants.HEIGHT)
    borders_list.add(vert_lane)
    all_sprite_list.add(vert_lane) 

"""
def handle_collision_with_borders():

    # Did the player moving caused collision with a border?
    borders_hit_list = pygame.sprite.spritecollide(player.sprite,borders_list,False)

    print(borders_hit_list)
"""
#-------------------------------------------------------------

# Groups
player = PlayerCar((constants.RBT_RIGHT_CENTER[0],constants.RBT_LEFT_CENTER[1]+2.5*constants.LANE_W))

buttons_list = DashboardButton.create_buttons_list()
buttons_group = pygame.sprite.Group(buttons_list)

level_tracker = LevelTracker()

#borders_list = pygame.sprite.Group()
#other_cars_list = pygame.sprite.Group()
#other_cars_list.add(player)

#player_car = PlayerCar(5,3)

#create_scene_borders(borders_list, playerGroup)
#-------------------------------------------------------------------------
running = True
# Game Loop
while running:
    # Limit our window to this max speed
    clock.tick(constants.FPS)   

    draw(constants.WIN,player)
    #feedback_tracker.update()
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

    move_player(player)
    
    #handle_collisions_with_road_borders(player)
    handle_collision_with_finish_line(player)
    
    # Update the window with everything we have drawn
    pygame.display.update()

    

#print(path)
#print(score)

#print(*pygame.font.get_fonts(), sep = "\n")

pygame.quit()   # Close the game cleanly