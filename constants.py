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

# Color Definitions
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Asset Definitions
SKY = scale_image(pygame.image.load(PATH + "Backgrounds/background0.png"),1)
SCENE = scale_image(pygame.image.load(PATH + "Scenes\scene_1.png"),1.4)
LEVEL_IMGS = [(SKY, (0,0)), (SCENE, (0,HEIGHT/10))]

DASHBOARD = scale_image(pygame.image.load(PATH + "Dashboard/dashboard.png"),0.8)
SPEEDOMETER = scale_image(pygame.image.load(PATH + "Dashboard/speedometer.png"),0.35)
MIRROR = scale_image(pygame.image.load(PATH + "Dashboard/rear_view_mirror.png"),0.27)
PHONE = scale_image(pygame.image.load(PATH + "Dashboard/phone.png"),0.55)

DASH_IMGS = [(DASHBOARD, (-70,460)), (SPEEDOMETER, (225,400)), (MIRROR, (WIDTH/2-200,-65)),(PHONE, (940,10))]

RED_CAR = scale_image(pygame.image.load(PATH + "Cars/red_car.png"), 0.3)

"""
SCENE_BORDER = scale_image(pygame.image.load("Assets\Images\Borders\Mishmar HaGvul_Border_Monocrome.png"),1.7)
# Create a mask from track border
SCENE_MASK = pygame.mask.from_surface(SCENE_BORDER)
"""

# Other Definitions
FPS = 60    # Frame per second

RADIUS = 45
