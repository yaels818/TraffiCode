# Outsource imports
import pygame

# Local imports
from utils import scale_image

pygame.font.init()

#main_font = pygame.font.SysFont("Eras Bold ITC", 20)
MAIN_FONT = pygame.font.SysFont("centurygothic", 36)
SMALL_FONT = pygame.font.SysFont("erasdemiitc", 26)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

BACKGROUND = scale_image(pygame.image.load("Assets\Images\Backgrounds/background0.png"),1)
SCENE = scale_image(pygame.image.load("Assets\Images\Scenes\scene_1.png"),1.35)
SCENE_BORDER = scale_image(pygame.image.load("Assets\Images\Borders\Mishmar HaGvul_Border_Monocrome.png"),1.7)
RED_CAR = scale_image(pygame.image.load("Assets\Images\Cars/red_car.png"), 0.5)

# Create a mask from track border
SCENE_MASK = pygame.mask.from_surface(SCENE_BORDER)

FPS = 60    # Frame per second