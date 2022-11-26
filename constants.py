# Outsource Imports
import pygame
import os

# Local Imports
from utils import scale_image

PATH = "Assets\Images/"

# Screen Definitions
WIDTH, HEIGHT = 1200, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.display.set_caption("TraffiCode")
pygame.display.set_icon(scale_image(pygame.image.load(PATH + "gameIcon.png"),0.2))

# Font Definitions
pygame.font.init()
MAIN_FONT = pygame.font.SysFont("centurygothic", 36)
SMALL_FONT = pygame.font.SysFont("erasdemiitc", 26)

# Color Definitions (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (59, 56, 56)
PINK = (255, 174, 201)

# Asset Definitions
SKY = scale_image(pygame.image.load(PATH + "Backgrounds/background0.png"),1.3)
SCENE = scale_image(pygame.image.load(PATH + "Scenes\scene_1.png"),1.4)
LEVEL_IMGS = [(SKY, (0,0)), (SCENE, (0, HEIGHT/12))]

DASHBOARD_RECT_HOR = pygame.Rect(0, HEIGHT-HEIGHT/7, WIDTH,HEIGHT/4)
DASHBOARD_RECT_VER = pygame.Rect(WIDTH - WIDTH/4.5, 0, WIDTH/4, HEIGHT)
SPEEDOMETER = scale_image(pygame.image.load(PATH + "Dashboard/speedometer.png"),0.28)
MIRROR = scale_image(pygame.image.load(PATH + "Dashboard/rear_view_mirror.png"),0.25)
PHONE = scale_image(pygame.image.load(PATH + "Dashboard/phone.png"),0.55)

# Position Markers
SCENE_CENTER = (WIDTH - WIDTH/4.7)/2
MIRROR_CENTER = (WIDTH/2 + (WIDTH - WIDTH/4.7)/2)/2
DASHBOARD_HOR_TOP = HEIGHT-HEIGHT/7
PHONE_CENTER = WIDTH - WIDTH/9

# Position Definitions - center
SPEEDOMETER_POS = (MIRROR_CENTER-SPEEDOMETER.get_rect().centerx, DASHBOARD_HOR_TOP-SPEEDOMETER.get_rect().centery/2)
MIRROR_POS = (MIRROR_CENTER-MIRROR.get_rect().centerx, -MIRROR.get_rect().centery/1.5)
PHONE_POS = (PHONE_CENTER-PHONE.get_rect().centerx,HEIGHT-DASHBOARD_HOR_TOP-PHONE.get_rect().centery/4)

DASH_IMGS = [(SPEEDOMETER, SPEEDOMETER_POS), (MIRROR, MIRROR_POS),(PHONE, PHONE_POS)]

RED_CAR = scale_image(pygame.image.load(PATH + "Cars/red_car.png"), 0.3)

# Other Definitions
FPS = 60    # Frame per second

RADIUS = 45

def draw_screen_positions():
    # Vertical
    pygame.draw.line(WIN, RED, (WIDTH/2, 0), (WIDTH/2, HEIGHT), 1)  # Half screen
    pygame.draw.line(WIN, BLUE, (WIDTH - WIDTH/9, 0), (WIDTH - WIDTH/9, HEIGHT), 1) # Phone center
    pygame.draw.line(WIN, BLUE, (WIDTH - WIDTH/4.7, 0), (WIDTH - WIDTH/4.7, HEIGHT), 1) # Phone Left
    pygame.draw.line(WIN, BLUE, ((WIDTH/2 + (WIDTH - WIDTH/4.7)/2)/2, 0), ((WIDTH/2 + (WIDTH - WIDTH/4.7)/2)/2, HEIGHT), 1) # Mirror center
    pygame.draw.line(WIN, RED, (SCENE_CENTER, 0), (SCENE_CENTER, HEIGHT), 1) # Scene center
    

    #print(PHONE.get_rect().center)
    
    #pygame.draw.line(WIN, BLUE, ((WIDTH - WIDTH/4.7)/2 + WIDTH/2, 0), (WIDTH/2-(WIDTH - WIDTH/4.7)/2, HEIGHT), 1) # Mirror center

    #pygame.draw.line(WIN, BLUE, (WIDTH/2 - WIDTH/4, 0), (WIDTH/2 - WIDTH/4, HEIGHT), 1) # Mirror center

    # Horizontal
    pygame.draw.line(WIN, RED, (0, HEIGHT/2), (WIDTH, HEIGHT/2), 1)
    pygame.draw.line(WIN, BLUE, (0, HEIGHT/3), (WIDTH, HEIGHT/3), 1)
    pygame.draw.line(WIN, GREEN, (0, HEIGHT/2 + HEIGHT/4), (WIDTH, HEIGHT/2 + HEIGHT/4), 1)
    pygame.draw.line(WIN, RED, (0, HEIGHT/2 - HEIGHT/4), (WIDTH, HEIGHT/2 - HEIGHT/4), 1)

    

