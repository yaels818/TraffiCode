# Outsource Imports
import pygame
import os

# Local Imports
from utils import scale_image

def load_button_images():
    
    for i in range(1,7):
        image_off = pygame.image.load("Assets\Images\Dashboard\Buttons\OFF/btn" + str(i) + ".png")
        image_on = pygame.image.load("Assets\Images\Dashboard\Buttons\ON/btn" + str(i) + ".png")
        BTN_IMGS_OFF.append(image_off)
        BTN_IMGS_ON.append(image_on)

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

# Other Definitions
FPS = 60    # Frame per second

RADIUS = 45

# Color Definitions (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (59, 56, 56)
PINK = (255, 174, 201)

# Position Markers - center x
SCENE_HEIGHT_START = HEIGHT/12
SCENE_CENTER = (WIDTH - WIDTH/4.7)/2
MIRROR_CENTER = (WIDTH/2 + (WIDTH - WIDTH/4.7)/2)/2
DASHBOARD_HOR_TOP = HEIGHT-HEIGHT/7
PHONE_CENTER = WIDTH - WIDTH/9
PHONE_LEFT = WIDTH - WIDTH/4.7
LIGHTS_BTN_CENTER = WIDTH-PHONE_CENTER

# Asset Definitions
SKY = scale_image(pygame.image.load(PATH + "Backgrounds/background0.png"),1.3)
SCENE = scale_image(pygame.image.load(PATH + "Scenes\scene_1.png"),1.4)
LEVEL_IMGS = [(SKY, (0,0)), (SCENE, (0, SCENE_HEIGHT_START))]

DASHBOARD_RECT_HOR = pygame.Rect(0, DASHBOARD_HOR_TOP, WIDTH,HEIGHT/4)
DASHBOARD_RECT_VER = pygame.Rect(WIDTH - WIDTH/4.5, 0, WIDTH/4, HEIGHT) 
SPEEDOMETER = scale_image(pygame.image.load(PATH + "Dashboard/speedometer.png"),0.3)
MIRROR = scale_image(pygame.image.load(PATH + "Dashboard/rear_view_mirror.png"),0.25)
PHONE = scale_image(pygame.image.load(PATH + "Dashboard/phone.png"),0.55)

# Position Definitions - center
SPEEDOMETER_POS = (MIRROR_CENTER-SPEEDOMETER.get_rect().centerx, DASHBOARD_HOR_TOP-SPEEDOMETER.get_rect().centery/2)
MIRROR_POS = (MIRROR_CENTER-MIRROR.get_rect().centerx, MIRROR.get_rect().centery/5)
PHONE_POS = (PHONE_CENTER-PHONE.get_rect().centerx,HEIGHT-DASHBOARD_HOR_TOP-PHONE.get_rect().centery/4)
DASH_IMGS = [(SPEEDOMETER, SPEEDOMETER_POS), (MIRROR, MIRROR_POS),(PHONE, PHONE_POS)]

# Dashboard Buttons Definitions
BTN_SCALE = 0.45
BLINKER_SCALE = 0.5
SPEEDOMETER_RIGHT = MIRROR_CENTER+SPEEDOMETER.get_rect().centerx
MENU_BTN_IMG = pygame.image.load("Assets\Images\Dashboard\Buttons/menu_btn.png")
BTN_IMGS_OFF = []
BTN_IMGS_ON = []

load_button_images()

MENU_BTN_POS = (MIRROR_CENTER/5, DASHBOARD_HOR_TOP-10)
LIGHTS_BTN_POS = (MIRROR_CENTER/2-BTN_IMGS_OFF[0].get_rect().centerx/2, DASHBOARD_HOR_TOP)

LEFT_BLINK_POS = (SPEEDOMETER_POS[0]-BTN_IMGS_OFF[1].get_rect().centerx ,DASHBOARD_HOR_TOP-10)
RIGHT_BLINK_POS = ((SPEEDOMETER_POS[0]+SPEEDOMETER_RIGHT)/2+BTN_IMGS_OFF[2].get_rect().centerx ,DASHBOARD_HOR_TOP-10)
#RIGHT_BLINK_POS = ((SPEEDOMETER_RIGHT+PHONE_CENTER)/3+BTN_IMGS_OFF[2].get_rect().centerx, DASHBOARD_HOR_TOP-10)

WIPERS_BTN_POS = (RIGHT_BLINK_POS[0]+BTN_IMGS_OFF[3].get_rect().centerx*1.5, DASHBOARD_HOR_TOP)
AC_BTN_POS = (WIPERS_BTN_POS[0]+BTN_IMGS_OFF[4].get_rect().centerx, DASHBOARD_HOR_TOP)
#AC_BTN_POS = (PHONE_LEFT-BTN_IMGS_OFF[4].get_rect().centerx/2, DASHBOARD_HOR_TOP)
#MUSIC_BTN_POS = (AC_BTN_POS[0]+BTN_IMGS_OFF[5].get_rect().centerx, DASHBOARD_HOR_TOP)
MUSIC_BTN_POS = (PHONE_CENTER-BTN_IMGS_OFF[5].get_rect().centerx/2, DASHBOARD_HOR_TOP)

MENU_BTN_BLP = [MENU_BTN_IMG,MENU_BTN_IMG,BTN_SCALE,*MENU_BTN_POS]
LIGHTS_BTN_BLP = [BTN_IMGS_OFF[0],BTN_IMGS_ON[0],BTN_SCALE,*LIGHTS_BTN_POS]
LEFT_BLINK_BLP = [BTN_IMGS_OFF[1],BTN_IMGS_ON[1],BLINKER_SCALE,*LEFT_BLINK_POS]
RIGHT_BLINK_BLP = [BTN_IMGS_OFF[2],BTN_IMGS_ON[2],BLINKER_SCALE,*RIGHT_BLINK_POS]
WIPERS_BTN_BLP = [BTN_IMGS_OFF[3],BTN_IMGS_ON[3],BTN_SCALE,*WIPERS_BTN_POS]
AC_BTN_BLP = [BTN_IMGS_OFF[4],BTN_IMGS_ON[4],BTN_SCALE,*AC_BTN_POS]
MUSIC_BTN_BLP = [BTN_IMGS_OFF[5],BTN_IMGS_ON[5],BTN_SCALE,*MUSIC_BTN_POS]



RED_CAR = scale_image(pygame.image.load(PATH + "Cars/red_car.png"), 0.3)


def draw_screen_positions():
    # Vertical
    pygame.draw.line(WIN, RED, (WIDTH/2, 0), (WIDTH/2, HEIGHT), 1)  # Half screen
    pygame.draw.line(WIN, BLUE, (WIDTH - WIDTH/9, 0), (WIDTH - WIDTH/9, HEIGHT), 1) # Phone center
    pygame.draw.line(WIN, BLUE, (WIDTH - WIDTH/4.7, 0), (WIDTH - WIDTH/4.7, HEIGHT), 1) # Phone Left
    pygame.draw.line(WIN, BLUE, (MIRROR_CENTER, 0), (MIRROR_CENTER, HEIGHT), 1) # Mirror center
    pygame.draw.line(WIN, RED, (SCENE_CENTER, 0), (SCENE_CENTER, HEIGHT), 1) # Scene center
    
    pygame.draw.line(WIN, GREEN, (MENU_BTN_POS[0],0), (MENU_BTN_POS[0], HEIGHT), 1)
    pygame.draw.line(WIN, GREEN, (LIGHTS_BTN_POS[0],0), (LIGHTS_BTN_POS[0], HEIGHT), 1)
    pygame.draw.line(WIN, GREEN, (LEFT_BLINK_POS[0],0), (LEFT_BLINK_POS[0], HEIGHT), 1)
    pygame.draw.line(WIN, GREEN, (SPEEDOMETER_POS[0],0), (SPEEDOMETER_POS[0], HEIGHT), 1)    
    pygame.draw.line(WIN, GREEN, (SPEEDOMETER_RIGHT,0), (SPEEDOMETER_RIGHT, HEIGHT), 1)
    pygame.draw.line(WIN, GREEN, (RIGHT_BLINK_POS[0],0), (RIGHT_BLINK_POS[0], HEIGHT), 1)
    pygame.draw.line(WIN, GREEN, (WIPERS_BTN_POS[0],0), (WIPERS_BTN_POS[0], HEIGHT), 1)
    pygame.draw.line(WIN, GREEN, (AC_BTN_POS[0],0), (AC_BTN_POS[0], HEIGHT), 1)

    pygame.draw.line(WIN, PINK, (WIDTH-PHONE_CENTER,0), (WIDTH-PHONE_CENTER, HEIGHT), 1)    # Left Parking Lot entry right
    pygame.draw.line(WIN, PINK, (MIRROR_CENTER/3,0), (MIRROR_CENTER/3, HEIGHT), 1)    # Left Parking Lot right boundary
    pygame.draw.line(WIN, PINK, (MIRROR_CENTER/2,0), (MIRROR_CENTER/2, HEIGHT), 1)    # Left Roundabout left line
    pygame.draw.line(WIN, PINK, (MIRROR_CENTER - (MIRROR_CENTER/2 - MIRROR_CENTER/4),0), (MIRROR_CENTER - (MIRROR_CENTER/2 - MIRROR_CENTER/4), HEIGHT), 1)    # Left Roundabout left line

    # Horizontal
    pygame.draw.line(WIN, RED, (0, HEIGHT/2), (WIDTH, HEIGHT/2), 1)
    pygame.draw.line(WIN, BLUE, (0, HEIGHT/3), (WIDTH, HEIGHT/3), 1)
    pygame.draw.line(WIN, GREEN, (0, HEIGHT/2 + HEIGHT/4), (WIDTH, HEIGHT/2 + HEIGHT/4), 1)
    pygame.draw.line(WIN, RED, (0, HEIGHT/2 - HEIGHT/4), (WIDTH, HEIGHT/2 - HEIGHT/4), 1)
    
