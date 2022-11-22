# Outsource imports
import pygame
import os
import math
from random import randint, choice

# Local imports
import constants
from RoadUsers import PlayerCar, PlayerSprite
from utils import *

pygame.init()
pygame.font.init()

# Load up a basic window
WIDTH, HEIGHT = 1200, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.display.set_caption("TraffiCode")
pygame.display.set_icon(scale_image(pygame.image.load("Assets\Images\gameIcon.png"),0.2))

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

class DashboardButton(pygame.sprite.Sprite):
    
    def __init__(self, image_off, image_on, scale, x_pos, y_pos):
        super(DashboardButton,self).__init__()

        self.image = scale_image(image_off,scale)
        self.scale = scale
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.pressed = False
        self.switch_image = scale_image(image_on,scale)

    def button_pressed(self):
        self.pressed = (not self.pressed)
        self.update_image()

    def update_image(self):
        temp = self.image
        self.image = self.switch_image
        self.switch_image = temp

#-------------------------------------------------------------

def draw(win, images, player_car):
    
    for img, pos in images:
        # Draw this img in this position
        win.blit(img, pos)  
    
    player_car.draw(win)
    
    #draw_points(path, win)
    #draw_scene_borders(win)
    draw_dashboard_init(win)


def draw_dashboard_init(win):
    
    path = "Assets\Images\Dashboard/"
    DASHBOARD = scale_image(pygame.image.load(path + "dashboard.png"),0.8)
    SPEEDOMETER = scale_image(pygame.image.load(path + "speedometer.png"),0.35)
    MIRROR = scale_image(pygame.image.load(path + "rear_view_mirror.png"),0.27)
    PHONE = scale_image(pygame.image.load(path + "phone.png"),0.55)
    
    elements = [(DASHBOARD, (-70,460)), (SPEEDOMETER, (225,400)), (MIRROR, (WIDTH/2-200,-65)),(PHONE, (940,10))]
    
    for img, pos in elements:
        # Draw this img in this position
        win.blit(img, pos)

    countdown_text = constants.SMALL_FONT.render(f"00:00:00", 1, constants.RED)
    #win.blit(countdown_text, (WIDTH/2-120,30))

    level_text = constants.SMALL_FONT.render(f"Level 1", 1, constants.RED)
    #win.blit(level_text, (860, 60))

    # round to the first significant digit, units are px/sec
    velocity_text = constants.SMALL_FONT.render(f"{round(player_car.vel, 1)}", 1, (255, 255, 255))
    win.blit(velocity_text, (360, HEIGHT - velocity_text.get_height() - 50))
#--------------------------------------------------------------

def move_player(player_car):
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a]:
        player_car.rotate(left = True)
    if keys[pygame.K_d]:
        player_car.rotate(right = True)
    if keys[pygame.K_w]:
        # While pressing Gas we do not want to slow
        moved = True 
        player_car.move_forward()
    if keys[pygame.K_s]:
        moved = True 
        player_car.move_backward()

    if not moved:
        player_car.reduce_speed()

def handle_collision_with_mask(player_car):
    # Check if the player car is colliding with the track walls
    if player_car.collide(constants.SCENE_MASK) != None:
        player_car.bounce()


# Function for drawing path points
def draw_points(path, win):
    for point in path:
        # Draw a red point of radius 5 in the path
        pygame.draw.circle(win, constants.RED, point, 5)

def draw_scene_borders(win):
    sidewalk_borders = [(("Top_Hori_Sidewalk"), (0, 185), (constants.SCENE.get_width(), 5)),
                        (("Bot_Hori_Sidewalk_Left"), (0, 380), (243, 5)),
                        (("Bot_Hori_Sidewalk_Right"), (437, 380), (constants.SCENE.get_width()-437, 5)),
                        (("Vert_Sidewalk_Left"), (constants.SCENE.get_width()-440, 380), (5, HEIGHT)),
                        (("Vert_Sidewalk_Right"), (437, 380), (5, HEIGHT))]


    lane_borders = [(("Hori_Lane"), (0, 285), (constants.SCENE.get_width(), 5)),
                    (("Vert_Lane"), ((int(constants.SCENE.get_width()/2)), 285), (5, HEIGHT))]

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

    vert_lane = Border('lane', int(constants.SCENE.get_width()/2), 285, 5, HEIGHT)
    borders_list.add(vert_lane)
    all_sprite_list.add(vert_lane) 

def handle_collision_with_borders():

    # Did the player moving caused collision with a border?
    borders_hit_list = pygame.sprite.spritecollide(player.sprite,borders_list,False)

    print(borders_hit_list)
#-------------------------------------------------------------

running = True
images = [(constants.BACKGROUND, (0,0)), (constants.SCENE, (0,HEIGHT/10))]

# Groups
player = PlayerSprite(3,2)

playerGroup = pygame.sprite.GroupSingle()
playerGroup.add(player)

borders_list = pygame.sprite.Group()
other_cars_list = pygame.sprite.Group()
other_cars_list.add(player)

player_car = PlayerCar(5,3)

create_scene_borders(borders_list, all_sprite_list)

#---------------------------------------------------------------

# load button images
button_images_off = []
button_images_on = []
for i in range(1,7):
    image_off = pygame.image.load("Assets\Images\Dashboard\Buttons\OFF/btn" + str(i) + ".png")
    image_on = pygame.image.load("Assets\Images\Dashboard\Buttons\ON/btn" + str(i) + ".png")
    button_images_off.append(image_off)
    button_images_on.append(image_on)

menu_btn_img = pygame.image.load("Assets\Images\Dashboard\Buttons/menu_btn.png")

lights_btn = DashboardButton(button_images_off[0], button_images_on[0], 0.55, 20, 500)
left_blinker_btn = DashboardButton(button_images_off[1], button_images_on[1], 0.65, 110, 480)
right_blinker_btn = DashboardButton(button_images_off[2], button_images_on[2],0.65, 485, 480)
wipers_btn = DashboardButton(button_images_off[3], button_images_on[3], 0.55, 620, 500)
ac_btn = DashboardButton(button_images_off[4], button_images_on[4], 0.55, 740, 500)
music_btn = DashboardButton(button_images_off[5], button_images_on[5], 0.55, 860, 500)
menu_btn = DashboardButton(menu_btn_img, menu_btn_img, 0.55, 980, 480)

buttons_group = pygame.sprite.Group()
buttons_group.add(lights_btn, left_blinker_btn, right_blinker_btn, wipers_btn, 
                ac_btn, music_btn, menu_btn)
RADIUS = 45

buttons_list = []
for button in buttons_group:
    buttons_list.append(button)
#-------------------------------------------------------------------------
# Game Loop
while running:
    # Limit our window to this max speed
    clock.tick(constants.FPS)   

    #draw(WIN, images, player_car)
    draw(WIN,images,player)
    buttons_group.draw(WIN)
    
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
                if (dis < RADIUS):
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