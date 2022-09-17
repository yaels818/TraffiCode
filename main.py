import pygame
import os
import math
from random import randint, choice
from utils import *


pygame.init()
#pygame.mixer.init()
#pygame.font.init()

# Load up a basic window
WIDTH, HEIGHT = 1100, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.display.set_caption("TraffiCode")
pygame.display.set_icon(scale_image(pygame.image.load("Assets\Images\gameIcon.png"),0.2))

#main_font = pygame.font.SysFont("Eras Bold ITC", 20)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

BACKGROUND = scale_image(pygame.image.load("Assets\Images\Backgrounds/background0.png"),0.76)
SCENE = scale_image(pygame.image.load("Assets\Images\Scenes\Mishmar HaGvul.png"),1.7)
SCENE_BORDER = scale_image(pygame.image.load("Assets\Images\Borders\Mishmar HaGvul_Border_Monocrome.png"),1.7)
RED_CAR = scale_image(pygame.image.load("Assets\Images\Cars/red_car.png"), 0.5)

# Create a mask from track border
SCENE_MASK = pygame.mask.from_surface(SCENE_BORDER)

FPS = 60    # Frame per second
clock = pygame.time.Clock()

score = 0

path = []

#-------------------------------------------------------------

class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.08 

    def rotate(self, left = False, right = False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate_center(win,self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        # Increase velocity without going over maximum velocity
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        # We want the max velocity backwards to be half of the max velocity forward
        # (Reverse gear cant reach top speed like forward gears)
        self.vel = max(self.vel - self.acceleration, -self.max_vel / 2)
        self.move()

    def move(self):
        # Using basic Trigonometry, calculate vertical and horizontal movement 
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        # Move the car in whatever direction it is facing
        self.y -= vertical
        self.x -= horizontal

    def collide(self, mask, x = 0, y = 0):
        car_mask = pygame.mask.from_surface(self.img)

        # Calculate displacement between the 2 masks
        offset = (int(self.x - x), int(self.y - y))

        # Point of intersection - if there was poi, the objects did collide
        poi = mask.overlap(car_mask, offset) 
        return poi

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0

class Player(AbstractCar, pygame.sprite.Sprite):

    IMG = RED_CAR
    START_POS = (150,150)

    def __init__(self):
        # Call the parent class's constructor
        pygame.sprite.Sprite.__init__(self)
        AbstractCar.__init__(self,2,2)
        self.image = RED_CAR
        self.rect = self.image.get_rect(center = self.START_POS)

    def reduce_speed(self):
        # Reduce the velocity by half the acceleration, if negative then just stop moving 
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self):
        # Bounce back from a wall
        self.vel = -self.vel/2
        self.move()

    def reset(self):
         AbstractCar().reset()

class PlayerCar(AbstractCar): # Inherit from AbstractCar
    IMG = RED_CAR
    START_POS = (400, 450)

    def reduce_speed(self):
        # Reduce the velocity by half the acceleration, if negative then just stop moving 
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self):
        # Bounce back from a wall
        self.vel = -self.vel/2
        self.move()

    def reset(self):
        super().reset()

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
            self.image.fill(RED)
        elif type == 'island':
            self.image.fill(WHITE)
        elif type == 'lane':
            self.image.fill(GREEN)

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

    # Update the window with everything we have drawn
    pygame.display.update() 

def draw_dashboard_init(win):
    path = "Assets\Images\Dashboard/"
    DASHBOARD = scale_image(pygame.image.load(path + "dashboard.png"),0.8)
    SPEEDOMETER = scale_image(pygame.image.load(path + "speedometer.png"),0.35)
    MIRROR = scale_image(pygame.image.load(path + "rear_view_mirror.png"),0.3)
    PHONE = scale_image(pygame.image.load(path + "phone.png"),0.53)
    
    elements = [(DASHBOARD, (-70,460)), (SPEEDOMETER, (225,400)), (MIRROR, (WIDTH/2-200,-65)),(PHONE, (840,10))]
    
    for img, pos in elements:
        # Draw this img in this position
        win.blit(img, pos)

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
    if player_car.collide(SCENE_MASK) != None:
        player_car.bounce()


# Function for drawing path points
def draw_points(path, win):
    for point in path:
        # Draw a red point of radius 5 in the path
        pygame.draw.circle(win, RED, point, 5)

def draw_scene_borders(win):
    sidewalk_borders = [(("Top_Hori_Sidewalk"), (0, 185), (SCENE.get_width(), 5)),
                        (("Bot_Hori_Sidewalk_Left"), (0, 380), (243, 5)),
                        (("Bot_Hori_Sidewalk_Right"), (437, 380), (SCENE.get_width()-437, 5)),
                        (("Vert_Sidewalk_Left"), (SCENE.get_width()-440, 380), (5, HEIGHT)),
                        (("Vert_Sidewalk_Right"), (437, 380), (5, HEIGHT))]


    lane_borders = [(("Hori_Lane"), (0, 285), (SCENE.get_width(), 5)),
                    (("Vert_Lane"), ((int(SCENE.get_width()/2)), 285), (5, HEIGHT))]

    island_borders = [(("Left_Island"), (135,273), (218-135,298-273)),
                    (("Bot_Island"), (300,381), (380-300,463-381))]

    for kind, top_left, bottom_right in sidewalk_borders:
        # Draw this kind in this position
        pygame.draw.rect(win, GREEN, (*top_left, *bottom_right))
    
    for kind, top_left, bottom_right in lane_borders:
        # Draw this kind in this position
        pygame.draw.rect(win, BLUE, (*top_left, *bottom_right))

    for kind, top_left, bottom_right in island_borders:
        # Draw this kind in this position
        pygame.draw.rect(win, RED, (*top_left, *bottom_right))
    #pygame.display.update() 
    
def create_scene_borders(borders_list, all_sprite_list):

    """
    top_hori_sidewalk = Border('sidewalk',0, 185, SCENE.get_width(), 5)
    borders_list.add(top_hori_sidewalk)
    all_sprite_list.add(top_hori_sidewalk)

    bot_hori_sidewalk_left = Border('sidewalk',0, 380, 243, 5)
    borders_list.add(bot_hori_sidewalk_left)
    all_sprite_list.add(bot_hori_sidewalk_left)    
    """

    hori_lane = Border('lane', 0, 285, SCENE.get_width(), 5)
    borders_list.add(hori_lane)
    all_sprite_list.add(hori_lane) 

    vert_lane = Border('lane', int(SCENE.get_width()/2), 285, 5, HEIGHT)
    borders_list.add(vert_lane)
    all_sprite_list.add(vert_lane) 

def handle_collision_with_borders():

    # Did the player moving caused collision with a border?
    borders_hit_list = pygame.sprite.spritecollide(player.sprite,borders_list,False)

    print(borders_hit_list)
#-------------------------------------------------------------

running = True
images = [(BACKGROUND, (0,0)), (SCENE, (0,0))]

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

borders_list = pygame.sprite.Group()
all_sprite_list = pygame.sprite.Group()
all_sprite_list.add(player)

player_car = PlayerCar(2,2)

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
    clock.tick(FPS)   

    draw(WIN, images, player_car)
    
    buttons_group.draw(WIN)
    
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

    # move_player(player_car)
    #move_player(player)
    #handle_collision_with_mask(player_car)
    #handle_collision_with_borders()

    pygame.display.update()

#print(path)
#print(score)

pygame.quit()   # Close the game cleanly