"""
Author: @yaels818
Description: TraffiCode - Practice driving from a new perspective
"""

# Imports
import pygame, math
import constants, DashboardButton
from LevelTracker import LevelTracker
from RoadUsers import PlayerCar, OtherCar, Pedestrian
from utils import *
from export_scores import export_data_to_file

pygame.init()
pygame.mixer.init()

#-------------------------------------------------------------
def draw_game(player_car):
    """
    Draw the level scene, finish line, player car, dashboard, level status. 

    Parameters
    ----------
    player_car : PlayerCar
        The car the player drives
    """    
    def draw_scene(curr_level):
        """
        Draw the scene for the current level (sky, scene/roads, street names).

        Parameters
        ----------
        curr_level : int
            The number of the current level
        """
        
        scene = constants.SCENE_LIGHT

        # Set the sky according to the current level (morning, noon, afternoon, night)
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
        
        # Draw each image in its position
        for img, pos in level_imgs:
            constants.WIN.blit(img, pos)  

        constants.draw_street_names()
    
    def draw_finish_line(curr_level):
        """
        Draw the finish line for the current level.

        Finish line is either a line to be crossed, 
        or a parking spot to be occupied by the player's car.

        Parameters
        ----------
        curr_level : int
            The number of the current level
        """
        # Get the current level's finish line's image and position
        img = constants.FINISH_LINE_IMGS[curr_level-1][0]
        pos = constants.FINISH_LINE_IMGS[curr_level-1][1]

        # Draw the respective finish line for this level -
        # finish line is either horizontal or vertical or a parking spot
        if img == "HORI":
            constants.WIN.blit(constants.FINISH_LINE_HORI, pos)
        elif img == "VERT":
            constants.WIN.blit(constants.FINISH_LINE_VERT,pos)
        else:
            # If finish line is a parking spot - draw a rectangle
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

    #TODO: delete helper functions
    #constants.draw_borders()
    #constants.draw_finish_lines()
    #constants.draw_masks()

    draw_dashboard()

    # Display the clipboard area (current level, violations, bonus points)
    level_tracker.display()
    
#--------------------------------------------------------------
def move_player(player_car):
    """
    Move the player's car according to the keyboard keys pressed.

    Parameters
    ----------
    player_car : PlayerCar
        The car the player drives
    """
    # Get which keyboard keys are being pressed
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
            # If player is moving in reverse gear 
            # -> lateral direction is reversed
            player_car.rotate(right = True)

    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        if not reverse_gear:
            player_car.rotate(right = True)
        else:
            # If player is moving in reverse gear 
            # -> lateral direction is reversed
            player_car.rotate(left = True)

    # If the player did not press for gas
    # -> the car should naturally lose speed (gradually) 
    if not gas_pressed:
        player_car.reduce_speed(emergency_brake = False)
#--------------------------------------------------------------

def handle_collision_with_finish_line(player_car):
    """
    Check if player's car reached the current level's finish line.

    Parameters
    ----------
    player_car : PlayerCar
        The car the player drives
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
        # If img == "PARKING" ==> rectangle is already stored inside pos
        finish_line_rect = pos
    
    # Check if player_car's center is colliding with finish_line_rect
    # (if the player crossed the finish line)
    if finish_line_rect.collidepoint(player_car.rect.center):
        if img != "PARKING":
            success_sound.play()
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
                            # If direction for this parking spot is NORTH
                            # ==> We need to check both 0 and 360 degrees
                            if direction == constants.NORTH:
                                if player_car.angle > (direction+360) - constants.DIRECTION_SMOOTH and \
                                    player_car.angle < (direction+360) + constants.DIRECTION_SMOOTH:
                                    level_tracker.add_accurate_parking()
                        
                        # Player gets to advance to the next level
                        # (even if the paraking is not accurate)
                        success_sound.play()
                        level_tracker.increase_level()
                        break

def handle_collisions_with_road_borders(player_car):
    """
    Check if player's car hit any road borders
    (parking lot walls, roundabout borders, sidewalk borders, solid lane borders).

    Parameters
    ----------
    player_car : PlayerCar
        The car the player drives
    """
    def check_mask_collisions(player_car, mask):
        """
        Check if the player's car is colliding with any of the masks 
        defined for this level (parking lot walls, roundabout borders).

        Parameters
        ----------
        player_car : PlayerCar
            The car the player drives
        
        mask : Mask
            The contours of the area's borders

        Notes
        -------
        Masks are a good solution for enforcing more complex borders 
        like roundabouts and parking lot walls, but the main drawback is 
        that this method is very heavy on the CPU (due to pixel-by-pixel comparison).
        To limit the stress to the CPU as much as possible, 
        we run the check on the masks only when the player is actually 
        within their area.         
        """
        
        # Check if the player car is colliding with the given mask
        # (poi = point of intersection)
        poi = player_car.check_collision_with_mask(mask)

        # If there is a collision
        if poi != None:
            # Stop the player's car (like it hit a wall)
            player_car.vel = 0
            # Draw the point of intersection
            pygame.draw.circle(constants.WIN, constants.RED, poi, 2)
            return True
        
        return False

    # Middle is the line between Yaar and Hadas 
    # (from top to bottom)
    VERT_MID_POINT = constants.YAAR_ROAD_BOT_L[0]

    # If player is on the RIGHT side of the scene
    if player_car.x > VERT_MID_POINT:
        area_rect = constants.RIGHT_PL_BORDER_RECT
        pl_mask = constants.MASKS[2]
        rbt_x = constants.RBT_RIGHT_CENTER[0]
        rbt_y = constants.RBT_RIGHT_CENTER[1]
        rbt_mask = constants.MASKS[3]

    # If player is on the LEFT side of the scene
    else:
        area_rect = constants.LEFT_PL_BORDER_RECT
        pl_mask = constants.MASKS[0]
        rbt_x = constants.RBT_LEFT_CENTER[0]
        rbt_y = constants.RBT_LEFT_CENTER[1]
        rbt_mask = constants.MASKS[1]

    # Track mask collisions
    # ----------------------
    # Check if player_car is within this side's parking lot
    if area_rect.contains(player_car.rect):
        if check_mask_collisions(player_car, pl_mask):
            level_tracker.add_parking_lot_hit()
    else:
        # Calculate the distance between player_car and the center of this side's roundabout
        dist_rbt = math.sqrt((rbt_x-player_car.x)**2 + (rbt_y-player_car.y)**2)
        # Check if player_car is within this side's roundabout
        if dist_rbt < constants.RBT_OUTER_RAD:
            if check_mask_collisions(player_car, rbt_mask):
                level_tracker.add_roundabout_hit()
    
    # Track rect collisions
    # ----------------------
        else:
            # Check if player_car is colliding with these roads' sidewalks
            # (These are horizontal so doesn't matter if RIGHT or LEFT)
            if player_car.rect.collidelist(constants.EREZ_ROAD_BORDERS) != -1:
                #print("collision, EREZ")
                level_tracker.add_sidewalk_hit()
            elif player_car.rect.collidelist(constants.ESHEL_ROAD_BORDERS) != -1:
                #print("collision, ESHEL")
                level_tracker.add_sidewalk_hit()
            else:
                # If player is on the RIGHT side of the scene
                if player_car.x > VERT_MID_POINT:
                    
                    if player_car.rect.collidelist(constants.ROTEM_ROAD_BORDERS) != -1:
                        #print("collision, ROTEM")
                        level_tracker.add_sidewalk_hit()

                    elif player_car.rect.collidelist(constants.YAAR_ROAD_BORDERS) != -1:
                        #print("collision, YAAR")
                        level_tracker.add_sidewalk_hit()

                    elif player_car.rect.collidelist(constants.SOLID_LANE_BORDERS) != -1:
                        #print("collision, SOLID")
                        level_tracker.add_over_solid_lane()

                # If player is on the LEFT side of the scene
                else:

                    if player_car.rect.collidelist(constants.HADAS_ROAD_BORDERS) != -1:
                        #print("collision, HADAS")
                        level_tracker.add_sidewalk_hit()
                
                    elif player_car.rect.collidelist(constants.ELLA_ROAD_BORDERS) != -1:
                        #print("collision, ELLA")
                        level_tracker.add_sidewalk_hit()

                    elif player_car.rect.collidelist(constants.SHAKED_ROAD_BORDERS) != -1:
                        #print("collision, SHAKED")
                        level_tracker.add_sidewalk_hit()

def handle_driving_against_traffic(player_car):
    """
    Check if player's car is headed against the road's direction.

    Parameters
    ----------
    player_car : PlayerCar
        The car the player drives
    """

    # Middle x is the line in the middle of Yaar
    # (the solid lane line, vertical)
    VERT_MID_POINT = constants.YAAR_SIDEW_BOT_L[0]

    # Middle y is the line at the bottom of Shaked (horizontal)
    HORI_MID_POINT = constants.SHAKED_SIDEWK_BOT_R[1]

    player_center = player_car.rect.center
    direction = player_car.angle

    # If player is on the RIGHT side of the scene
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
level_tracker = LevelTracker(10)
clock = pygame.time.Clock()
time_counter = 0

# Sprites (moving objects)
player = PlayerCar()

buttons_list = DashboardButton.create_buttons_list()
buttons_group = pygame.sprite.Group(buttons_list)

other_cars_group = pygame.sprite.Group()
peds_group = pygame.sprite.Group()

# Sounds
"""
pygame.mixer.music.load("Sounds/bgm.wav")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)
"""

crash_ped_sound = pygame.mixer.Sound("Assets\Sounds/tires_squeal.wav")
crash_ped_sound.set_volume(0.3)

success_sound = pygame.mixer.Sound("Assets\Sounds/success.wav")
success_sound.set_volume(0.3)
#-------------------------------------------------------------------------

# Main Game Loop
running = True
while running:
    # Limit our window to this max speed 
    # (display this amount of Frames Per Second so the game 
    # would run at the same speed on computers with different processing power)
    clock.tick(constants.FPS)   

    # Run a seperate, in-game counter 
    # ------------------------------------------------
    time_counter += 1
    # Check if a full cycle is done (1 sec)
    if time_counter == constants.FPS:
        # Track when it's time to add more sprites
        level_tracker.increase_timer_to_add_sprites()

        # Add a new pedestrian every time_between_peds seconds  
        if level_tracker.timer_to_add_sprites != 0 and \
            level_tracker.timer_to_add_sprites % level_tracker.time_between_peds == 0:
            peds_group.add(Pedestrian(level_tracker.peds_vel))
            
        # Add a new passing car every time_between_cars seconds  
        if level_tracker.timer_to_add_sprites != 0 and \
            level_tracker.timer_to_add_sprites % level_tracker.time_between_cars == 0:
            other_cars_group.add(OtherCar(level_tracker.cars_vel))

        # Reset the counter (for the next second)
        time_counter = 0

    # Draw the game elements, buttons and pedestrians
    # ------------------------------------------------
    draw_game(player)
    buttons_group.draw(constants.WIN)
    peds_group.draw(constants.WIN)       

    # Track input events
    # ------------------------------------------------
    for event in pygame.event.get():
        # If player clicked X on the game window
        if event.type == pygame.QUIT:   
            # Stop the game loop
            running = False
            break 

        # If player pressed a keyboard key
        if event.type == pygame.KEYDOWN:
            # Get which keys were pressed
            keys = pygame.key.get_pressed()
            # Once the player starts moving the car
            # --> Start the level's timer
            if keys[pygame.K_w] or keys[pygame.K_s]:
                if not level_tracker.level_started:
                    level_tracker.start_level()
            # Activate blinkers by key press
            if keys[pygame.K_q]:
                buttons_list[2].button_pressed() # Left blinker
            if keys[pygame.K_e]:
                buttons_list[3].button_pressed() # Right blinker

        # If player clicked the left mouse button 
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get current mouse position
            m_x, m_y = pygame.mouse.get_pos()
            pos = pygame.mouse.get_pos()
            
            # Helper array and function to build peds and cars paths
            #other.path_exp.append(pos)
            
            # Check if one of the dashboard buttons was pressed
            for button in buttons_list:
                # Calculate the distance between mouse position and the center of the button
                dis = math.sqrt((button.rect.centerx-m_x)**2 + (button.rect.centery-m_y)**2)
                #pygame.draw.circle(WIN, RED, (button.rect.centerx, button.rect.centery), RADIUS)
                if (dis < constants.RADIUS):
                    button.button_pressed()

    # Move all the sprites (player, other cars, peds)
    # -----------------------------------------------
    move_player(player)
    
    for car in other_cars_group:
        car.draw()
        #car.draw_points(constants.RED)
        car.move_sprite()

    for ped in peds_group:
        #ped.draw_points(constants.PINK)
        ped.move_sprite()
    
    # Handle collisions between player and sprites
    # -----------------------------------------------
    # Check collision between player and any of the peds. 
    # If there is collision, remove the ped and track the violation. 
    for item in pygame.sprite.spritecollide(player,peds_group,True):
            level_tracker.add_ped_hit()
            crash_ped_sound.play()

    # Check collision between player and any of the cars. 
    # If there is collision, remove the car and track the violation. 
    for item in pygame.sprite.spritecollide(player,other_cars_group,True):
            level_tracker.add_car_hit()

    # Handle collisions between player and static objects
    # ----------------------------------------------------
    handle_collision_with_finish_line(player)
    #handle_collisions_with_road_borders(player)
    handle_driving_against_traffic(player)

    # Update the window with everything we have drawn
    pygame.display.update()

    
    # If player finished the last level
    # ----------------------------------------------------
    if level_tracker.game_finished():
        text = "THANK YOU FOR PLAYING, YOU WON THE GAME!"
        blit_text_center(constants.WIN, constants.MAIN_FONT, constants.ORANGE, text)
        pygame.display.update()
        pygame.time.delay(3000)

        # 
        export_data_to_file(level_tracker.tracking_table)
        
        level_tracker.reset()
        player.reset()
        peds_group.empty()
        other_cars_group.empty()

#print(other.path_exp)

pygame.quit()   # Close the game cleanly