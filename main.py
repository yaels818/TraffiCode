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

# Initializations
pygame.init()
pygame.mixer.init()

#-------------------------------------------------------------
def draw_game(player_car, is_menu_button_pressed):
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
        if curr_level <= constants.LAST_LEVEL_SKY_DAY:
            sky = constants.SKY_DAY 
        elif curr_level <= constants.LAST_LEVEL_SKY_SUNNY:
            sky = constants.SKY_SUNNY
        elif curr_level <= constants.LAST_LEVEL_SKY_RAINY:
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

        # Get the player's velocity (in px/sec) and round it to the first significant digit and double by 10 
        # (To get a reasonable km/hr velocity)
        velocity_text = constants.DASH_FONT.render(f"{round(round(player.vel,1)*10.0)}", 1, (255, 255, 255))

        # Calculate the position for the velocity text
        # (Center of the speedometer)
        velocity_text_pos = (constants.SPEEDOMETER_TEXT_POS[0]-velocity_text.get_rect().centerx,constants.SPEEDOMETER_TEXT_POS[1]-velocity_text.get_rect().centery)
        
        # Draw the dashboard text (how fast the player's car is moving)
        constants.WIN.blit(velocity_text, velocity_text_pos) 

    draw_scene(level_tracker.level)

    draw_finish_line(level_tracker.level)
    
    player_car.draw()

    #TODO: delete helper functions
    #constants.draw_borders()
    #constants.draw_finish_lines()
    #constants.draw_masks()

    draw_dashboard()

    # If the player started moving
    # -> Display on the clipboard area
    if level_tracker.level_started:
        if is_menu_button_pressed:
            level_tracker.display_instructions()
        else:
            level_tracker.display_score()
    else:
        level_tracker.display_instructions()

def draw_start_or_end_screen(is_start_screen):
    if is_start_screen:
        #Display the menu background
        """
        sky = scale_image(pygame.image.load("Assets\Images\Backgrounds\day_sky.jpg"),0.3)
        scene = scale_image(pygame.image.load("Assets\Images\Scenes\Mishmar HaGvul.png"),constants.SCENE_SCALE)
        """
        screen = constants.START_SCREEN
    else:
        screen = constants.END_SCREEN


    """
    level_imgs = [(sky, (0,0)), (scene, (constants.MIRROR_POS[0], constants.SCENE_HEIGHT_START))]
        
    # Draw each image in its position
    for img, pos in level_imgs:
        constants.WIN.blit(img, pos)  
    """
    constants.WIN.blit(screen, (0,0))  
    pygame.display.flip()

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

    if keys[pygame.K_w]:
        gas_pressed = True 
        reverse_gear = False
        player_car.move_forward()

    if keys[pygame.K_s]:
        gas_pressed = True 
        reverse_gear = True
        player_car.move_backward() 

    if keys[pygame.K_a]:
        if not reverse_gear:
            player_car.rotate(left = True)
        else:
            # If player is moving in reverse gear 
            # -> lateral direction is reversed
            player_car.rotate(right = True)

    if keys[pygame.K_d]:
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

def handle_collision_with_finish_line(player_car, parking_button):
    """
    Check if player's car reached the current level's finish line.

    Parameters
    ----------
    player_car : PlayerCar
        The car the player drives

    parking_button : DashboardButton
        The parking button on the dashboard

    Notes
    -----
    1. Finish line can either be a line to cross or a parking spot to park in.
    2. If it is a line - check if player crossed it (in any direction).
    3. If it is a parking spot - if parking button is pressed, 
    check if player is inside it and if the car's angle is accurate 
    in relation with the spot's direction 
    (depending on level instructions or road direction).
    4. The angle does not have to be 100% accurate - we use some smoothing 
    to allow a small degree of inaccuracy that is still acceptable (=considered accurate).
    5. If the angle is accurate - player gets bonus points. 
    """
    # Get the current finish line's index 
    curr_finish_line = level_tracker.level - 1

    # Get the current finish line's image and position
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
        # If img == "PARKING" 
        # ==> Rectangle is already stored inside pos
        finish_line_rect = pos
    
    # Check if player_car's center is colliding with finish_line_rect
    if finish_line_rect.collidepoint(player_car.rect.center):
        if img != "PARKING":
            # Player crossed the finish line
            success_sound.play()
            level_tracker.increase_level()
        else:
            # If player car is parked
            if parking_button.pressed:
                for direction, p_spot in constants.FINISH_LINE_PARKINGS:
                    # Identify the current parking spot
                    if finish_line_rect.topleft == p_spot.topleft:
                        # Check if the player_car's angle while parked is accurate
                        # for this specific parking spot 
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
        #pl_mask = constants.MASKS[0]   # Disabled left pl mask - known issue
        pl_mask = constants.MASKS[1]
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
    #-------------------------------------------------------------
    if player_center[0] > VERT_MID_POINT:

        area_rect = constants.RIGHT_PL_BORDER_RECT

        # player is at the top-right of the screen
        #-----------------------------------------
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
            
        # player is at the bottom-right
        #-----------------------------------------
        else:
            if area_rect.contains(player_car.rect):
                return

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
                  
    # If player is on the LEFT side of the scene
    #-------------------------------------------------------------
    else:

        area_rect = constants.LEFT_PL_BORDER_RECT

        # player is at the top-left of the screen
        #-----------------------------------------
        if player_center[1] < HORI_MID_POINT:
            
            # Erez, left side
            if player_center >= constants.ELLA_ROAD_BORDERS[0].topleft and \
                player_center <= constants.SOLID_LANE_BORDERS[0].bottomright:

                if direction < constants.NORTH_WEST or direction > constants.SOUTH:
                    level_tracker.add_driving_against_traffic()
        
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
        #-----------------------------------------
        else:

            if area_rect.contains(player_car.rect):
                return

            # entering Ella from Left PL or Eshel
            if player_center >= constants.ELLA_ROAD_BORDERS[1].topleft and \
                player_center <= constants.ELLA_ROAD_BORDERS[4].bottomright:
                # direction is not upwards or sideways
                if direction > 90 and direction < 270:
                    level_tracker.add_driving_against_traffic()

#--------------------------------------------------------------
def handle_dash_button_press(btn_index):
    
    buttons_list[btn_index].button_pressed() 

    if btn_index == constants.MUSIC_BTN_INDEX:
        if buttons_list[btn_index].pressed:
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.fadeout(2000)
    elif btn_index == constants.LEFT_BLINK_INDEX or btn_index == constants.RIGHT_BLINK_INDEX:
        if buttons_list[btn_index].pressed:
            car_blinker_sound.play()
    elif btn_index == constants.LIGHTS_BTN_INDEX:
        if buttons_list[btn_index].pressed and level_tracker.level > constants.LAST_LEVEL_SKY_RAINY:
            pass
    elif btn_index == constants.WIPERS_BTN_INDEX:
        if buttons_list[btn_index].pressed and \
            level_tracker.level > constants.LAST_LEVEL_SKY_SUNNY and \
                level_tracker.level <= constants.LAST_LEVEL_SKY_RAINY:
            pass

#-------------------------------------------------------------
# Screens Management
is_start_screen = True
is_finish_screen = False
#-------------------------------------------------------------
# Game Management Objects
level_tracker = LevelTracker()
clock = pygame.time.Clock()
time_counter = 0

#-------------------------------------------------------------
# Sprites (moving objects)
player = PlayerCar()

buttons_list = DashboardButton.create_buttons_list()
buttons_group = pygame.sprite.Group(buttons_list)

other_cars_group = pygame.sprite.Group()
peds_group = pygame.sprite.Group()

#-------------------------------------------------------------
# Sounds
buttons_list[constants.MUSIC_BTN_INDEX].button_pressed()
pygame.mixer.music.load(constants.MAIN_SOUND_TRAFFIC)
pygame.mixer.music.set_volume(constants.MAIN_SOUND_VOL)
pygame.mixer.music.play(-1)

crash_ped_sound = pygame.mixer.Sound(constants.SOUND_TIRES_SQUEAL)
crash_ped_sound.set_volume(constants.SOUND_EFFECT_VOL)

crash_car_sound = pygame.mixer.Sound(constants.SOUND_CAR_CRASH)
crash_car_sound.set_volume(constants.SOUND_EFFECT_VOL)

car_blinker_sound = pygame.mixer.Sound(constants.SOUND_CAR_BLINKER)
car_blinker_sound.set_volume(constants.SOUND_EFFECT_VOL)

success_sound = pygame.mixer.Sound(constants.SOUND_SUCCESS)
success_sound.set_volume(constants.SOUND_EFFECT_VOL)

#-------------------------------------------------------------------------
# Main Game Loop
#-------------------------------------------------------------------------
is_game_running = True
while is_game_running:
    
    # Game Start Screen 
    # ------------------------------------------------
    while is_start_screen:
        
        draw_start_or_end_screen(is_start_screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_start_screen = False
                is_game_running = False
                break
            
            #Pressing space starts the game ( runs main )
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    is_start_screen = False
    
    # Limit our window to this max speed 
    # (display this amount of Frames Per Second so the game 
    # would run at the same speed on computers with different processing power)
    clock.tick(constants.FPS)   

    # Run a seperate, in-game counter for sprite groups
    # --------------------------------------------------
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
    draw_game(player, buttons_list[constants.MENU_BTN_INDEX].pressed)
    buttons_group.draw(constants.WIN)
    peds_group.draw(constants.WIN)     

    # Track input events
    # ------------------------------------------------
    for event in pygame.event.get():
        # If player clicked X on the game window
        if event.type == pygame.QUIT:   
            # Stop the game loop
            is_game_running = False
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
                handle_dash_button_press(constants.LEFT_BLINK_INDEX)
            if keys[pygame.K_e]:
                handle_dash_button_press(constants.RIGHT_BLINK_INDEX)
            # Activate parking by key press
            if keys[pygame.K_p]:
                handle_dash_button_press(constants.PARKING_BTN_INDEX)

        # If player clicked the left mouse button 
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get current mouse position
            m_x, m_y = pygame.mouse.get_pos()
            pos = pygame.mouse.get_pos()
            
            # Helper array and function to build peds and cars paths
            #other.path_exp.append(pos)
            
            # Check if one of the dashboard buttons was pressed
            btn_index = 0
            for button in buttons_list:
                # Calculate the distance between mouse position and the center of the button
                dis = math.sqrt((button.rect.centerx-m_x)**2 + (button.rect.centery-m_y)**2)
                #pygame.draw.circle(WIN, RED, (button.rect.centerx, button.rect.centery), RADIUS)
                if (dis < constants.RADIUS):
                    handle_dash_button_press(btn_index)
                btn_index += 1

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
        text = "OH NO, YOU HIT A PEDESTRIAN!"
        pos = (5, constants.SCENE_HEIGHT_START)
        blit_text_in_pos(constants.WIN, constants.DASH_FONT, constants.RED, text, pos)
        pygame.display.update()
        pygame.time.delay(2000) # 3 seconds delay to the game (moment of silence)
        
    # Check collision between player and any of the cars. 
    # If there is collision, remove the car and track the violation. 
    for item in pygame.sprite.spritecollide(player,other_cars_group,True):
        level_tracker.add_car_hit()
        crash_car_sound.play()

    # Handle collisions between player and static objects
    # ----------------------------------------------------
    handle_collision_with_finish_line(player, buttons_list[constants.PARKING_BTN_INDEX])
    handle_collisions_with_road_borders(player)
    handle_driving_against_traffic(player)

    # Update the window with everything we have drawn
    pygame.display.update()

    # If player finished the last level
    # ----------------------------------------------------
    if level_tracker.game_finished():
        is_finish_screen = True
        pygame.mixer.music.fadeout(2000)
        pygame.mixer.music.load(constants.MAIN_SOUND_BOSSA)
        pygame.mixer.music.set_volume(constants.MAIN_SOUND_VOL)
        pygame.mixer.music.play(-1)

        # Game Finish Screen 
        # ------------------------------------------------
        while is_finish_screen:
            draw_start_or_end_screen(is_start_screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    export_data_to_file(level_tracker.tracking_table)
                    is_finish_screen = False
                    is_game_running = False
                    break
                
                # Pressing space restarts the game
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        export_data_to_file(level_tracker.tracking_table)

                        pygame.mixer.music.fadeout(2000)
                        pygame.mixer.music.load(constants.MAIN_SOUND_TRAFFIC)
                        pygame.mixer.music.set_volume(constants.MAIN_SOUND_VOL)
                        pygame.mixer.music.play(-1)

                        for button in buttons_list:
                            if button.pressed:
                                if button != buttons_list[constants.MUSIC_BTN_INDEX]:
                                    button.button_pressed()

                        level_tracker.reset()
                        player.reset()
                        peds_group.empty()
                        other_cars_group.empty()

                        is_start_screen = True
                        is_finish_screen = False

#print(other.path_exp)

pygame.quit()   # Close the game cleanly