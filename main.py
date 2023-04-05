# Outsource imports
"""
Author: Yael Sch
Description: TraffiCode - Driving challenges (with regards to traffic codes)
"""

# Outsource imports
import pygame, math, random

# Local imports
import constants, DashboardButton
from LevelTracker import LevelTracker
from RoadUsers import PlayerCar, OtherCar, Pedestrian
from utils import *

pygame.init()
pygame.font.init()

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

def draw(player_car):
    """
    Draw the level scene, finish line, player car, dashboard, level status. 

    Parameters
    ----------
    player_car : PlayerCar
        The car the player drives
    """
    def draw_scene(curr_level):
        """
        Draw the scene for the current level (sky, roads, street names).

        Parameters
        ----------
        curr_level : int
            The number of the current level
    
        """
        # TODO: insert random and change skies and dark/light
        LEVEL_IMGS = [(constants.SKY_DAY, (0,0)), (constants.SCENE, (0, constants.SCENE_HEIGHT_START))]
        
        for img, pos in LEVEL_IMGS:
            # Draw this img in this position
            constants.WIN.blit(img, pos)  

        constants.draw_street_names()
        
    def draw_finish_line(curr_level):
        """
        Draw the finish line for the current level.

        Finish line is either a line to be crossed, 
        or a parking spot to be filled, by the player's car.

        Parameters
        ----------
        curr_level : int
            The number of the current level
    
        """
        # Get the current level's finish line's image and position
        img = constants.FINISH_LINE_IMGS[curr_level-1][0]
        pos = constants.FINISH_LINE_IMGS[curr_level-1][1]

        if img == "HORI":
            constants.WIN.blit(constants.FINISH_LINE_HORI, pos)
        elif img == "VERT":
            constants.WIN.blit(constants.FINISH_LINE_VERT,pos)
        else:
            # If finish line is a parking spot
            pygame.draw.rect(constants.WIN, constants.ORANGE, pos)

    def draw_dashboard():
        """
        Draw the dashboard elements and texts (excluding the buttons). 
        """

        # Draw the dashboard background
        for r in constants.DASH_RECTS:
            pygame.draw.rect(constants.WIN, constants.GRAY, r)
        
        # Draw the dashboard elements
        for img, pos in constants.DASH_IMGS:
            # Draw this img in this position
            constants.WIN.blit(img, pos)

        # Draw the dashboard text (how fast the player's car is moving)
        # (Round to the first significant digit, units are px/sec)
        velocity_text = constants.DASH_FONT.render(f"{round(round(player.vel,1)*10.0)}", 1, (255, 255, 255))
        velocity_text_pos = (constants.SPEEDOMETER_TEXT_POS[0]-velocity_text.get_rect().centerx,constants.SPEEDOMETER_TEXT_POS[1]-velocity_text.get_rect().centery)
        constants.WIN.blit(velocity_text, velocity_text_pos) 

    
    draw_scene(level_tracker.level)

    draw_finish_line(level_tracker.level)
    
    player_car.draw(constants.WIN)

    #draw_points(path, win)
    #constants.draw_borders()
    #constants.draw_finish_lines()

    draw_dashboard()

    # Display the clipboard area (current level, violations, bonus points)
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

def handle_collision_with_finish_line(player_car):
    """
    
    """

    curr_finish_line = level_tracker.level - 1

    img = constants.FINISH_LINE_IMGS[curr_finish_line][0]
    pos = constants.FINISH_LINE_IMGS[curr_finish_line][1]

    # get the rectangle of the finish line for this level
    # then move it to the right coordinates
    if img == "HORI":
        finish_line_rect = constants.FINISH_LINE_HORI.get_rect().copy()
        finish_line_rect.move_ip(pos)
    elif img == "VERT":
        finish_line_rect = constants.FINISH_LINE_VERT.get_rect().copy()
        finish_line_rect.move_ip(pos)
    else:
        # img == "PARKING" ==> rect is inside pos
        finish_line_rect = pos.copy()
        #finish_line_rect.move_ip(finish_line_rect.topleft)

    # check collision
    if img != "PARKING":
        # check if player_car's center is colliding with finish_line_rect -
        # if the player crossed the finish line
        if finish_line_rect.collidepoint(player_car.rect.center):
            level_tracker.increase_level()
    else:
        player_center = player_car.rect.center
        direction = player_car.angle

        # check if player_car is completely inside the parking spot
        if finish_line_rect.contains(player_car.rect):
            print("good")
        else:
            pass
        

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

    # middle is between Yaar and Hadas
    VERT_MID_POINT = constants.YAAR_ROAD_BOT_L[0]

    #player_car_rect = player_car.rect
    #pygame.draw.circle(constants.WIN, constants.GREEN, player_car.rect.center, 2)
    #player_car_rect.inflate_ip(-0.5,-0.5)
    #pygame.draw.rect(constants.WIN,constants.PINK, player_car_rect,4)

    # player is on the right side of the scene
    if player_car.x > VERT_MID_POINT:
        # count mask collisions
        # check if player_car is completely inside the parking lot
        if constants.RIGHT_PL_BORDER_RECT.contains(player_car.rect):
            if check_mask_collisions(player_car, constants.MASK_RIGHT_PL):
                level_tracker.add_parking_lot_hit()
        else:
            dis_right_rbt = math.sqrt((constants.RBT_RIGHT_CENTER[0]-player_car.x)**2 + \
                                    (constants.RBT_RIGHT_CENTER[1]-player_car.y)**2)
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
        # count solid lanes collisions
                elif player_car.rect.collidelist(constants.SOLID_LANE_BORDERS) != -1:
                    print("collision, SOLID")
                    level_tracker.add_over_solid_lane()
                        
    # player is on the left side
    else:
        # count mask collisions
        #if player_car.x < constants.ELLA_ROAD_TOP_L[0] and player_car.y > constants.SHAKED_SIDEWK_BOT_R[1]:
        # check if player_car is completely inside the parking lot
        if constants.LEFT_PL_BORDER_RECT.contains(player_car.rect):
            if check_mask_collisions(player_car, constants.MASK_LEFT_PL):
                level_tracker.add_parking_lot_hit()
        else:
            dis_left_rbt = math.sqrt((constants.RBT_LEFT_CENTER[0]-player_car.x)**2 + \
                                    (constants.RBT_LEFT_CENTER[1]-player_car.y)**2)
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

def handle_driving_against_traffic(player_car):
    """
    """

    # middle x is middle of Yaar (solid lane line)
    VERT_MID_POINT = constants.YAAR_SIDEW_BOT_L[0]

    # middle y is shaked sidewalk bottom line
    HORI_MID_POINT = constants.SHAKED_SIDEWK_BOT_R[1]

    player_center = player_car.rect.center
    direction = player_car.angle

    # player is on the right side of the scene
    if player_center[0] > VERT_MID_POINT:
        # player is at the top-right of the screen
        if player_center[1] < HORI_MID_POINT:
            # Erez, right side (top)
            if player_center >= constants.SOLID_LANE_BORDERS[0].topright and \
                player_center <= constants.EREZ_ROAD_BORDERS[7].topleft and \
                player_center[1] < constants.EREZ_LANE_BORDERS[0].top:

                if direction > constants.SOUTH_WEST and direction < constants.NORTH_EAST:
                    level_tracker.add_driving_against_traffic()
                    
            # Erez, right side (bottom)
            elif player_center >= constants.SOLID_LANE_BORDERS[0].topright and \
                player_center <= constants.EREZ_LANE_BORDERS[1].topleft and \
                player_center[1] > constants.EREZ_LANE_BORDERS[0].bottom:
                print("b")
                if direction < constants.SOUTH or direction > constants.NORTH_EAST:
                    level_tracker.add_driving_against_traffic()

            # entering Erez from Yaar  #TODO : DEBUG HERE  
            elif player_center >= constants.SOLID_LANE_BORDERS[1].bottomright and \
                player_center <= constants.YAAR_ROAD_BORDERS[6].topleft :
                print("x")
                if direction > constants.WEST and direction < constants.EAST:
                    level_tracker.add_driving_against_traffic()   
        
        # player is at the bottom-right
        else:
            # Rotem (top)
            if player_center >= constants.ROTEM_ROAD_BORDERS[0].topleft and \
                player_center <= constants.ROTEM_LANE_BORDERS[0].bottomright and \
                player_center[1] < constants.ROTEM_LANE_BORDERS[0].top:

                if direction > constants.SOUTH_WEST and direction < constants.NORTH_EAST:
                    level_tracker.add_driving_against_traffic()
            
            # Rotem (bottom)
            elif player_center >= constants.ROTEM_ROAD_BORDERS[0].topleft and \
                player_center <= constants.ROTEM_LANE_BORDERS[0].bottomright and \
                player_center[1] > constants.ROTEM_LANE_BORDERS[0].bottom:

                #if direction < constants.SOUTH_WEST or direction > constants.NORTH_EAST:
                if direction < constants.SOUTH or direction > constants.NORTH_EAST:
                    level_tracker.add_driving_against_traffic()
                  
    # player is on the left side
    else:
        # player is at the top-left of the screen
        if player_center[1] < HORI_MID_POINT:
            
            # Erez, left side
            if player_center >= constants.ELLA_ROAD_BORDERS[0].topleft and \
                player_center <= constants.SOLID_LANE_BORDERS[0].bottomright:

                if direction < constants.NORTH_WEST or direction > constants.SOUTH:
                    level_tracker.add_driving_against_traffic()
        
            # entering Yaar from Erez #TODO : DEBUG HERE  
            elif player_center >= constants.YAAR_ROAD_BORDERS[4].topleft and \
                player_center <= constants.SOLID_LANE_BORDERS[1].bottomright:
                
                if direction < constants.WEST or direction > constants.SOUTH_EAST:
                    level_tracker.add_driving_against_traffic()
                    print("x")
            # entering Hadas from Erez
            elif player_center >= constants.HADAS_ROAD_BORDERS[0].topleft and \
                player_center <= constants.HADAS_ROAD_BORDERS[2].bottomright:
                
                if direction < constants.SOUTH_WEST or direction > constants.SOUTH_EAST:
                    level_tracker.add_driving_against_traffic()
            
            # entering Ella from Erez
            elif player_center >= constants.ELLA_ROAD_BORDERS[0].topleft and \
                player_center <= constants.ELLA_ROAD_BORDERS[3].bottomright:
                # direction is not downwards
                if direction < constants.SOUTH_WEST or direction > constants.SOUTH_EAST:
                    level_tracker.add_driving_against_traffic()
        
        # player is at the bottom-left
        else:
            # entering Yaar from Hadas or Erez
            
            # entering Ella from Left PL or Eshel
            if player_center >= constants.ELLA_ROAD_BORDERS[1].topleft and \
                player_center <= constants.ELLA_ROAD_BORDERS[4].bottomright:
                # direction is not upwards or sideways
                if direction > 90 and direction < 270:
                    level_tracker.add_driving_against_traffic()


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

# Game Management Objects
level_tracker = LevelTracker()
clock = pygame.time.Clock()

# Sprites (moving objects)
player = PlayerCar()
other = OtherCar()
ped = Pedestrian()

buttons_list = DashboardButton.create_buttons_list()
buttons_group = pygame.sprite.Group(buttons_list)

other_cars_list = pygame.sprite.Group()
other_cars_list.add(other)

peds_list = pygame.sprite.Group()
peds_list.add(ped)

#create_scene_borders(borders_list, playerGroup)
#-------------------------------------------------------------------------
# Main Game Loop
running = True
while running:
    # Limit our window to this max speed
    clock.tick(constants.FPS)   

    draw(player)
    
    buttons_group.draw(constants.WIN)
    #other_cars_list.draw(constants.WIN)
    #peds_list.draw(constants.WIN)

    for event in pygame.event.get():
        # If player clicked X on the window
        if event.type == pygame.QUIT:   
            running = False
            break 

        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_w] or keys[pygame.K_s]:
                if not level_tracker.level_started:
                    level_tracker.start_level()
            if keys[pygame.K_q]:
                buttons_list[1].button_pressed() # left blinker
            if keys[pygame.K_e]:
                buttons_list[2].button_pressed() # right blinker

        # If player clicked with left mouse button 
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get current mouse position
            m_x, m_y = pygame.mouse.get_pos()
            pos = pygame.mouse.get_pos()
            #other.draw_points(constants.WIN)
            other.path_exp.append(pos)
            # Check if one of the dashboard buttons was pressed
            for button in buttons_list:
                dis = math.sqrt((button.rect.centerx-m_x)**2 + (button.rect.centery-m_y)**2)
                #pygame.draw.circle(WIN, RED, (button.rect.centerx, button.rect.centery), RADIUS)
                if (dis < constants.RADIUS):
                    button.button_pressed()
            
    #other.draw_points(constants.WIN)
    move_player(player)
    
    for car in other_cars_list:
        #car.move()
        pass

    for ped in peds_list:
        ped.move()
        #pass
        
    handle_collision_with_finish_line(player)
    #handle_collisions_with_road_borders(player)
    #handle_driving_against_traffic(player)
    #handle_parallel_parking(player, constants.YAAR_PP_BORDERS[0].center)

    # Update the window with everything we have drawn
    pygame.display.update()

    

print(other.path_exp)

#print(*pygame.font.get_fonts(), sep = "\n")

pygame.quit()   # Close the game cleanly