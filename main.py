"""
Author: @yaels818
Description: TraffiCode - Practice your driving from a new perspective, 

"""

# Imports
import pygame, math
import constants, DashboardButton
from LevelTracker import LevelTracker
from RoadUsers import PlayerCar, OtherCar, Pedestrian
from utils import *

pygame.init()

#-------------------------------------------------------------
def draw_game(player_car):
    """
    Draw the level scene, finish line, player car, dashboard, level status. 

    Parameters
    ----------
    player_car : PlayerCar
        The car the player drives
    
    Returns
    -------
    None
    """    
    def draw_scene(curr_level):
        """
        Draw the scene for the current level (sky, roads, street names).

        Parameters
        ----------
        curr_level : int
            The number of the current level

        """
        
        scene = constants.SCENE_LIGHT

        if curr_level <= 3:
            sky = constants.SKY_DAY
        elif curr_level <= 5:
            sky = constants.SKY_SUNNY
        elif curr_level <= 8:
            sky = constants.SKY_RAINY
        else:
            sky = constants.SKY_NIGHT
            scene = constants.SCENE_DARK

        level_imgs = [(sky, (0,0)), (scene, (0, constants.SCENE_HEIGHT_START))]
        
        for img, pos in level_imgs:
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
    
    player_car.draw()

    #constants.draw_borders()
    #constants.draw_finish_lines()
    #constants.draw_masks()

    draw_dashboard()

    # Display the clipboard area (current level, violations, bonus points)
    level_tracker.display()
    
#--------------------------------------------------------------
def move_player(player_car):
    """
    Move the player_car according to the keyboard keys pressed 

    Parameters
    ----------
    player_car : PlayerCar
        The car the player drives
    
    Returns
    -------
    None
    """
    # Get which keyboard keys are pressed
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

    # If player did not press on gas, the car should lose speed naturally 
    if not gas_pressed:
        player_car.reduce_speed(emergency_brake = False)
#--------------------------------------------------------------

def handle_collision_with_finish_line(player_car):
    """
    Check if player reached the current level's finish line

    Parameters
    ----------
    player_car : PlayerCar
        The car the player drives
    
    Returns
    -------
    None
    """
    # Get the current finish line's index 
    curr_finish_line = level_tracker.level - 1

    img = constants.FINISH_LINE_IMGS[curr_finish_line][0]
    pos = constants.FINISH_LINE_IMGS[curr_finish_line][1]
    
    if img == "HORI":
        # Copy the rectangle of the finish line for this level
        finish_line_rect = constants.FINISH_LINE_HORI.get_rect().copy()
        # Move the copy to the correct position
        finish_line_rect.move_ip(pos)
    elif img == "VERT":
        # Copy the rectangle of the finish line for this level
        finish_line_rect = constants.FINISH_LINE_VERT.get_rect().copy()
        # Move the copy to the correct position
        finish_line_rect.move_ip(pos)
    else:
        # If img == "PARKING" ==> rectangle is stored inside pos
        finish_line_rect = pos
    
    # Check if player_car's center is colliding with finish_line_rect.
    # Meaning, if the player crossed the finish line
    if finish_line_rect.collidepoint(player_car.rect.center):
        if img != "PARKING":
            # Player gets to advance to the next level
            level_tracker.increase_level()
        else:
            # If player car is parked
            if player_car.vel == 0:
                for direction, p_spot in constants.FINISH_LINE_PARKINGS:
                    # Identify the current parking spot
                    if finish_line_rect.topleft == p_spot.topleft:
                        # Check if the player_car's angle while parked is accurate
                        # for this specific parking spot
                        # (depending on level instructions or road direction)
                        if player_car.angle > direction - constants.DIRECTION_SMOOTH and \
                            player_car.angle < direction + constants.DIRECTION_SMOOTH:
                            level_tracker.add_accurate_parking()
                        else:
                            # If direction for this parking spot is NORTH, 
                            # we need to check both 0 and 360 degrees
                            if direction == constants.NORTH:
                                if player_car.angle > (direction+360) - constants.DIRECTION_SMOOTH and \
                                    player_car.angle < (direction+360) + constants.DIRECTION_SMOOTH:
                                    level_tracker.add_accurate_parking()
                        
                        level_tracker.increase_level()
                        break

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
        # If there is some point of intersection 
        if poi != None:
            player_car.vel = 0
            pygame.draw.circle(constants.WIN, constants.RED, poi, 2)
            return True
        return False

    # middle is between Yaar and Hadas
    VERT_MID_POINT = constants.YAAR_ROAD_BOT_L[0]

    # player is on the right side of the scene
    if player_car.x > VERT_MID_POINT:
        # count mask collisions
        # check if player_car is completely inside the right parking lot
        if constants.RIGHT_PL_BORDER_RECT.contains(player_car.rect):
            if check_mask_collisions(player_car, constants.MASKS[2]):
                level_tracker.add_parking_lot_hit()
        else:
            dis_right_rbt = math.sqrt((constants.RBT_RIGHT_CENTER[0]-player_car.x)**2 + \
                                    (constants.RBT_RIGHT_CENTER[1]-player_car.y)**2)
            if dis_right_rbt < constants.RBT_OUTER_RAD:
                if check_mask_collisions(player_car, constants.MASKS[3]):
                    level_tracker.add_roundabout_hit()
            else:
        # count regular collisions
                if player_car.rect.collidelist(constants.ROTEM_ROAD_BORDERS) != -1:
                    #print("collision, ROTEM")
                    level_tracker.add_sidewalk_hit()
                elif player_car.rect.collidelist(constants.EREZ_ROAD_BORDERS) != -1:
                    #print("collision, EREZ")
                    level_tracker.add_sidewalk_hit()
                elif player_car.rect.collidelist(constants.YAAR_ROAD_BORDERS) != -1:
                    #print("collision, YAAR")
                    level_tracker.add_sidewalk_hit()
        # count solid lanes collisions
                elif player_car.rect.collidelist(constants.SOLID_LANE_BORDERS) != -1:
                    #print("collision, SOLID")
                    level_tracker.add_over_solid_lane()
                        
    # player is on the left side
    else:
        # count mask collisions
        #if player_car.x < constants.ELLA_ROAD_TOP_L[0] and player_car.y > constants.SHAKED_SIDEWK_BOT_R[1]:
        # check if player_car is completely inside the parking lot
        if constants.LEFT_PL_BORDER_RECT.contains(player_car.rect):
            #if check_mask_collisions(player_car, constants.MASKS[0]):
                #level_tracker.add_parking_lot_hit()
            pass
        else:
            dis_left_rbt = math.sqrt((constants.RBT_LEFT_CENTER[0]-player_car.x)**2 + \
                                    (constants.RBT_LEFT_CENTER[1]-player_car.y)**2)
            if dis_left_rbt < constants.RBT_OUTER_RAD:
                if check_mask_collisions(player_car, constants.MASKS[1]):
                    level_tracker.add_roundabout_hit()
            else:
        # count regular collisions
                if player_car.rect.collidelist(constants.HADAS_ROAD_BORDERS) != -1:
                    #print("collision, HADAS")
                    level_tracker.add_sidewalk_hit()
                elif player_car.rect.collidelist(constants.EREZ_ROAD_BORDERS) != -1:
                    #print("collision, EREZ")
                    level_tracker.add_sidewalk_hit()
                elif player_car.rect.collidelist(constants.ELLA_ROAD_BORDERS) != -1:
                    #print("collision, ELLA")
                    level_tracker.add_sidewalk_hit()
                elif player_car.rect.collidelist(constants.SHAKED_ROAD_BORDERS) != -1:
                    #print("collision, SHAKED")
                    level_tracker.add_sidewalk_hit()
                elif player_car.rect.collidelist(constants.ESHEL_ROAD_BORDERS) != -1:
                    #print("collision, ESHEL")
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
                #print("b")
                if direction < constants.SOUTH or direction > constants.NORTH_EAST:
                    level_tracker.add_driving_against_traffic()

            # entering Erez from Yaar  #TODO : DEBUG HERE  
            elif player_center >= constants.SOLID_LANE_BORDERS[1].bottomright and \
                player_center <= constants.YAAR_ROAD_BORDERS[6].topleft :
                #print("x")
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
                    #print("x")
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

#-------------------------------------------------------------
# Game Management Objects
level_tracker = LevelTracker(1)
clock = pygame.time.Clock()
time_counter = 0

# Sprites (moving objects)
player = PlayerCar()

buttons_list = DashboardButton.create_buttons_list()
buttons_group = pygame.sprite.Group(buttons_list)

other_cars_group = pygame.sprite.Group()
peds_group = pygame.sprite.Group()

#-------------------------------------------------------------------------

# Main Game Loop
running = True
while running:
    # Limit our window to this max speed (display this many Frames Per Second)
    # (so the game would run equally on computers with different processing power)
    clock.tick(constants.FPS)   

    # Run a seperate, in-game counter
    time_counter += 1
    if time_counter == constants.FPS:
        level_tracker.increase_timer_to_add_sprites()
        # Adds peds every TIME_BETWEEN_PEDS seconds  
        if level_tracker.timer_to_add_sprites != 0 and \
            level_tracker.timer_to_add_sprites % level_tracker.time_between_peds == 0:
            peds_group.add(Pedestrian(level_tracker.peds_vel))
            
        # Adds peds every TIME_BETWEEN_PEDS seconds  
        if level_tracker.timer_to_add_sprites != 0 and \
            level_tracker.timer_to_add_sprites % level_tracker.time_between_cars == 0:
            other_cars_group.add(OtherCar(level_tracker.cars_vel))

        time_counter = 0

    draw_game(player)
    buttons_group.draw(constants.WIN)
    peds_group.draw(constants.WIN)       

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
                buttons_list[2].button_pressed() # left blinker
            if keys[pygame.K_e]:
                buttons_list[3].button_pressed() # right blinker

        # If player clicked with left mouse button 
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get current mouse position
            m_x, m_y = pygame.mouse.get_pos()
            pos = pygame.mouse.get_pos()
            
            #other.path_exp.append(pos)
            
            # Check if one of the dashboard buttons was pressed
            for button in buttons_list:
                dis = math.sqrt((button.rect.centerx-m_x)**2 + (button.rect.centery-m_y)**2)
                #pygame.draw.circle(WIN, RED, (button.rect.centerx, button.rect.centery), RADIUS)
                if (dis < constants.RADIUS):
                    button.button_pressed()

    move_player(player)
    
    for car in other_cars_group:
        car.draw()
        #car.draw_points(constants.RED)
        car.move_sprite()

    for ped in peds_group:
        #ped.draw_points(constants.PINK)
        ped.move_sprite()
    
    # Check collision between player and any of the peds. 
    # If there is collision, remove the ped and track the violation. 
    for item in pygame.sprite.spritecollide(player,peds_group,True):
            level_tracker.add_ped_hit()

    # Check collision between player and any of the cars. 
    # If there is collision, remove the ped and track the violation. 
    for item in pygame.sprite.spritecollide(player,other_cars_group,True):
            level_tracker.add_car_hit()

    handle_collision_with_finish_line(player)
    handle_collisions_with_road_borders(player)
    handle_driving_against_traffic(player)

    # Update the window with everything we have drawn
    pygame.display.update()

    
    # If player finished the last level
    if level_tracker.game_finished():
        text = "THANK YOU FOR PLAYING, YOU WON THE GAME!"
        blit_text_center(constants.WIN, constants.MAIN_FONT, constants.ORANGE, text)
        pygame.display.update()
        pygame.time.delay(3000)
        level_tracker.reset()
        player.reset()
        peds_group.empty()
        other_cars_group.empty()

#print(other.path_exp)

pygame.quit()   # Close the game cleanly