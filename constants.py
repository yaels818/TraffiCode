"""
Author: @yaels818
Description: Constants module, contains all constant definitions needed for the game, 
            and helper functions to draw them (some for dev only).
Notes: 
    Rect class (used to make rectangles in pygame): 
        Rect(left, top, width, height) -> Rect
        Rect((left, top), (width, height)) -> Rect
"""
# Imports
import pygame, os
from utils import scale_image, stretch_image
#-------------------------------------------------------------------------
# Helper Function (called within this module)
#--------------------------------------------
def load_buttons_images():
    """
    Load all the images (on and off) for the dashboard buttons. 
    """
    BTNS_DIR_IMGS = "Assets\Images\Dashboard\Buttons/"

    MENU_BTN_IMG = pygame.image.load(BTNS_DIR_IMGS + "menu_btn.png")

    BTN_IMGS_OFF.append(MENU_BTN_IMG)
    BTN_IMGS_ON.append(MENU_BTN_IMG)

    # Go over all the images in the directories,
    # load and add them to their lists
    for i in range(1,7):
        image_off = pygame.image.load(BTNS_DIR_IMGS + "OFF/btn" + str(i) + ".png")
        image_on = pygame.image.load(BTNS_DIR_IMGS + "ON/btn" + str(i) + ".png")

        BTN_IMGS_OFF.append(image_off)
        BTN_IMGS_ON.append(image_on)

def load_buttons_blueprints():
    """
    Load buttons blueprints for DashboardButton
    """
    # Buttons Blueprints for DashboardButton
    BTN_SCALE = 0.45
    BLINKER_SCALE = 0.5

    SPEEDOMETER_RIGHT = MIRROR_CENTER+SPEEDOMETER.get_rect().centerx

    y = DASHBOARD_HOR_TOP
    i = 1

    MENU_BTN_POS = (MIRROR_CENTER/5, y-10)    
    LIGHTS_BTN_POS = (MIRROR_CENTER/2-BTN_IMGS_OFF[i].get_rect().centerx/2, y)
    LEFT_BLINK_POS = (SPEEDOMETER_POS[0]-BTN_IMGS_OFF[i+1].get_rect().centerx ,y-10)
    RIGHT_BLINK_POS = ((SPEEDOMETER_POS[0]+SPEEDOMETER_RIGHT)/2+BTN_IMGS_OFF[i+2].get_rect().centerx ,y-10)
    WIPERS_BTN_POS = (RIGHT_BLINK_POS[0]+BTN_IMGS_OFF[i+3].get_rect().centerx*1.5, y)
    PARKING_BTN_POS = (WIPERS_BTN_POS[0]+BTN_IMGS_OFF[i+4].get_rect().centerx, y)
    MUSIC_BTN_POS = (CLIP_CENTER-BTN_IMGS_OFF[i+5].get_rect().centerx/2, y)

    BTNS_POSITIONS = [
        MENU_BTN_POS, LIGHTS_BTN_POS, LEFT_BLINK_POS, RIGHT_BLINK_POS,
        WIPERS_BTN_POS, PARKING_BTN_POS, MUSIC_BTN_POS]

    for i in range(len(BTNS_POSITIONS)):
        if i == LEFT_BLINK_INDEX or i == RIGHT_BLINK_INDEX:
            scale = BLINKER_SCALE
        else:
            scale = BTN_SCALE

        BTN_BLPS.append([BTN_IMGS_OFF[i], BTN_IMGS_ON[i], scale, *BTNS_POSITIONS[i]])

def load_masks():
    """
    Generate masks for all the complex areas in the game
    """
    BORDERS_DIR = DIR_IMGS + "Borders\Scene_1/"

    MASKS_IMGS_PATHS = [
        "mask_left_pl_wider_minus_wall", "mask_left_rbt_full", "mask_right_pl", "mask_right_rbt_full"]

    for path in MASKS_IMGS_PATHS:
        MASKS_IMGS.append(scale_image(pygame.image.load(BORDERS_DIR + path + ".png"),SCENE_SCALE))

    for m in MASKS_IMGS:
        MASKS.append(pygame.mask.from_surface(m))

#-------------------------------------------------------------------------
# Directory Paths
#----------------
DIR_IMGS = "Assets\Images/"
DIR_SOUNDS = "Assets\Sounds/"
#-------------------------------------------------------------------------
# Screen Definitions
#-------------------
WIDTH, HEIGHT = 1200, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.display.set_caption("TraffiCode")
pygame.display.set_icon(scale_image(pygame.image.load(DIR_IMGS + "gameIcon.png"),0.2))
#-------------------------------------------------------------------------
# Font Definitions
#-----------------
pygame.font.init()
MAIN_FONT = pygame.font.SysFont("centurygothic", 36)
DASH_FONT = pygame.font.SysFont("erasdemiitc", 26)
CLIP_FONT = pygame.font.SysFont("erasdemiitc", 19)
STREETS_FONT = pygame.font.SysFont("erasdemiitc", 12)
#-------------------------------------------------------------------------
# Sound Definitions
#------------------
MAIN_SOUND_VOL = 0.2
SOUND_EFFECT_VOL = 0.3

MAIN_SOUND_TRAFFIC = DIR_SOUNDS + "city_medium_traffic.mp3"
MAIN_SOUND_BOSSA = DIR_SOUNDS + "8bit_bossa_nova.mp3"

SOUND_TIRES_SQUEAL = DIR_SOUNDS + "tires_squeal.wav"
SOUND_CAR_CRASH = DIR_SOUNDS + "car_crash.wav"
SOUND_CAR_BLINKER = DIR_SOUNDS + "car_blinker.mp3"
SOUND_SUCCESS = DIR_SOUNDS + "success.wav"

#-------------------------------------------------------------------------
# Other Definitions
#------------------
FPS = 60    # Frame per second
RADIUS = 45
#-------------------------------------------------------------------------
# Color Definitions (RGB)
#------------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (59, 56, 56)
RED = (255, 0, 0)
GREEN = (64, 156, 98)
BLUE = (0, 0, 255)
PINK = (255, 174, 201)
ORANGE = (255,127,39)
#-------------------------------------------------------------------------
# Asset Definitions - Screens
#----------------------------
START_SCREEN = pygame.image.load(DIR_IMGS + "Screens/" + "start_screen.png")
END_SCREEN = pygame.image.load(DIR_IMGS + "Screens/" + "end_screen.png")
#-------------------------------------------------------------------------
# Asset Definitions - Scene
#---------------------------
SCENE_SCALE = 1.4

SKY_DAY = scale_image(pygame.image.load(DIR_IMGS + "Backgrounds/" + "day_sky.jpg"),0.25)
SKY_NIGHT = scale_image(pygame.image.load(DIR_IMGS + "Backgrounds/" + "night_sky.jpg"),0.5)
SKY_RAINY = scale_image(pygame.image.load(DIR_IMGS + "Backgrounds/" + "rainy_sky.jpg"),0.3)
SKY_SUNNY = scale_image(pygame.image.load(DIR_IMGS + "Backgrounds/" + "sunny_sky.jpg"),0.25)

SCENE_LIGHT = scale_image(pygame.image.load(DIR_IMGS + "Scenes\scene_1_light.png"),SCENE_SCALE)
SCENE_DARK = scale_image(pygame.image.load(DIR_IMGS + "Scenes\scene_1_dark.png"),SCENE_SCALE)

LAST_LEVEL_SKY_DAY = 3
LAST_LEVEL_SKY_SUNNY = 5
LAST_LEVEL_SKY_RAINY = 8

# Asset Definitions - Scene Masks
#---------------------------------
MASKS_IMGS = []
MASKS = []
load_masks()
#-------------------------------------------------------------------------
# Position Markers (Center X)
#-----------------------------
SCENE_HEIGHT_START = HEIGHT/12
SCENE_CENTER = (WIDTH - WIDTH/4.7)/2

SCENE_OFFSET = (0,SCENE_HEIGHT_START)

DASHBOARD_HOR_TOP = HEIGHT-HEIGHT/7
DASHBOARD_VERT_LEFT = WIDTH - WIDTH/4.5

CLIP_LEFT = WIDTH - WIDTH/4.7
CLIP_CENTER = WIDTH - WIDTH/8.5 
CLIP_TOP = HEIGHT/7.5

MIRROR_CENTER = (WIDTH/2 + (WIDTH - WIDTH/4.7)/2)/2
LIGHTS_BTN_CENTER = WIDTH-CLIP_CENTER
#-------------------------------------------------------------------------
# Asset Definitions - Dashboard
#------------------------------
DASH_RECTS = [
    # Horizontal
    pygame.Rect(0, DASHBOARD_HOR_TOP, WIDTH,HEIGHT/4),
    
    # Vertical
    pygame.Rect(WIDTH - WIDTH/4.5, 0, WIDTH/4, HEIGHT) 

    ]

SPEEDOMETER = scale_image(pygame.image.load(DIR_IMGS + "Dashboard/speedometer.png"),0.3)
MIRROR = scale_image(pygame.image.load(DIR_IMGS + "Dashboard/rear_view_mirror.png"),0.25)
CLIPBOARD = stretch_image(pygame.image.load(DIR_IMGS + "Dashboard/clipboard.png"),0.55,0.8)

SPEEDOMETER_POS = (MIRROR_CENTER-SPEEDOMETER.get_rect().centerx, DASHBOARD_HOR_TOP-SPEEDOMETER.get_rect().centery/2)
MIRROR_POS = (MIRROR_CENTER-MIRROR.get_rect().centerx, MIRROR.get_rect().centery/3)
CLIP_POS = (CLIP_CENTER-CLIPBOARD.get_rect().centerx,CLIP_TOP-CLIPBOARD.get_rect().centery/2.5)

DASH_IMGS = [(SPEEDOMETER, SPEEDOMETER_POS), (MIRROR, MIRROR_POS),(CLIPBOARD, CLIP_POS)]

SPEEDOMETER_TEXT_POS = (MIRROR_CENTER,SPEEDOMETER_POS[1]+SPEEDOMETER.get_rect().centery)
#-------------------------------------------------------------------------
# Dashboard Buttons Definitions
#------------------------------
BTN_IMGS_OFF = []
BTN_IMGS_ON = []
load_buttons_images()

MENU_BTN_INDEX = 0    
LIGHTS_BTN_INDEX = 1
LEFT_BLINK_INDEX = 2
RIGHT_BLINK_INDEX = 3
WIPERS_BTN_INDEX = 4
PARKING_BTN_INDEX = 5
MUSIC_BTN_INDEX = 6

BTN_BLPS = []
load_buttons_blueprints()
#-------------------------------------------------------------------------
# Road Definitions
#-----------------
LANE_W = 22 # Lane Width in px

MID_LEFT_BLINK_POS_X = MIRROR_CENTER-SPEEDOMETER.get_rect().centerx-BTN_IMGS_OFF[2].get_rect().centerx/2

    # Roads
YAAR_ROAD_BOT_L = (MID_LEFT_BLINK_POS_X, HEIGHT-HEIGHT/3+5)
YAAR_ROAD_MID_R = (YAAR_ROAD_BOT_L[0] + 4.2*LANE_W, HEIGHT-HEIGHT/3+5)
EREZ_ROAD_BOT_L = (MIRROR_CENTER/3+LANE_W, HEIGHT/6.2)
ELLA_ROAD_TOP_L = (MIRROR_CENTER/3+1,HEIGHT/6.2)
ESHEL_ROAD_BOT_R = (YAAR_ROAD_MID_R[0]+LANE_W,HEIGHT-HEIGHT/4+2)
ROTEM_ROAD_BOT_R = (MIRROR_CENTER*1.5-0.6*LANE_W,HEIGHT/2 - 0.2*LANE_W)

    # Sidewalks    
SHAKED_SIDEWK_BOT_R = (MIRROR_CENTER/2-4*LANE_W, HEIGHT/2 - 2.2*LANE_W)
EREZ_ROTEM_SIDEWK_TOP_R = (YAAR_ROAD_MID_R[0]+6*LANE_W, HEIGHT/6.2 + 2*LANE_W)
YAAR_SIDEW_BOT_L = (YAAR_ROAD_MID_R[0]-3.1*LANE_W, EREZ_ROTEM_SIDEWK_TOP_R[1]+2*LANE_W)

    # Roundabouts
RBT_LEFT_CENTER = (MIRROR_CENTER/2+LANE_W, SHAKED_SIDEWK_BOT_R[1]+LANE_W)
RBT_RIGHT_CENTER = (MIRROR_CENTER*1.5-2*LANE_W, EREZ_ROTEM_SIDEWK_TOP_R[1]+LANE_W)
RBT_OUTER_RAD = RADIUS+1.7*LANE_W
RBT_INNER_RAD = RADIUS-1.3*LANE_W
#-------------------------------------------------------------------------
# Borders Definitions
#--------------------
    # Parking Lots Outside Borders
LEFT_PL_BORDER_RECT = pygame.Rect((0, SHAKED_SIDEWK_BOT_R[1]+2*LANE_W), (SHAKED_SIDEWK_BOT_R[0], ESHEL_ROAD_BOT_R[1]-2*LANE_W-(SHAKED_SIDEWK_BOT_R[1]+2*LANE_W)))
RIGHT_PL_BORDER_RECT = pygame.Rect((EREZ_ROTEM_SIDEWK_TOP_R[0], SHAKED_SIDEWK_BOT_R[1]+2*LANE_W), (CLIP_LEFT-LANE_W-(EREZ_ROTEM_SIDEWK_TOP_R[0]), ESHEL_ROAD_BOT_R[1]-(SHAKED_SIDEWK_BOT_R[1]+1.5*LANE_W)))

    # Reverse Parking Borders
PLS_RP_BORDERS = [
    # Horizontal
        # Left PL, top left spot (FINISH_LINE_IMGS #4)
    pygame.Rect((0.35*LANE_W, SHAKED_SIDEWK_BOT_R[1]+4.1*LANE_W), (2*LANE_W, LANE_W)),
    
    # Vertical
        # Right PL, bottom right spot (FINISH_LINE_IMGS #5)
    pygame.Rect((ROTEM_ROAD_BOT_R[0]+2.75*LANE_W, ESHEL_ROAD_BOT_R[1]-2.25*LANE_W), (LANE_W, 2*LANE_W)),
    
    ]

    # Sidewalk Borders
EREZ_ROAD_BORDERS = [
    # Horizontal
        # Top (border with sky)
    pygame.Rect((MIRROR_CENTER/3, ELLA_ROAD_TOP_L[1]), (EREZ_ROTEM_SIDEWK_TOP_R[0]+2*LANE_W-(MIRROR_CENTER/3), 2)),
        # Top (border with park)
    pygame.Rect((EREZ_ROTEM_SIDEWK_TOP_R[0]+2*LANE_W, EREZ_ROTEM_SIDEWK_TOP_R[1]), (RBT_RIGHT_CENTER[0]-3.25*LANE_W-(EREZ_ROTEM_SIDEWK_TOP_R[0]+2*LANE_W), 2)),
        # Bottom - Ella till Hadas
    pygame.Rect((MIRROR_CENTER/3+LANE_W, EREZ_ROTEM_SIDEWK_TOP_R[1]), (MIRROR_CENTER/2-(MIRROR_CENTER/3+LANE_W), 2)),
        # Bottom - Hadas till Yaar
    pygame.Rect((MIRROR_CENTER/2+2*LANE_W+2, EREZ_ROTEM_SIDEWK_TOP_R[1]), (YAAR_ROAD_BOT_L[0]-(MIRROR_CENTER/2+2*LANE_W+2), 2)),
        # Bottom - Yaar Sidewalk
    pygame.Rect((YAAR_SIDEW_BOT_L[0], EREZ_ROTEM_SIDEWK_TOP_R[1]), (YAAR_ROAD_MID_R[0]-1.1*LANE_W-(YAAR_SIDEW_BOT_L[0]), 2)),
        # Bottom - Yaar till Erez 
    pygame.Rect((YAAR_ROAD_MID_R[0], EREZ_ROTEM_SIDEWK_TOP_R[1]), (EREZ_ROTEM_SIDEWK_TOP_R[0]-(YAAR_ROAD_MID_R[0]), 2)),
        # Bottom - Erez till Rotem
    pygame.Rect((EREZ_ROTEM_SIDEWK_TOP_R[0], EREZ_ROTEM_SIDEWK_TOP_R[1]+2*LANE_W), (RBT_RIGHT_CENTER[0]-3.25*LANE_W-(EREZ_ROTEM_SIDEWK_TOP_R[0]), 2)),
    # Vertical
            # Top - Erez till Rotem
    pygame.Rect((EREZ_ROTEM_SIDEWK_TOP_R[0]+2*LANE_W, ELLA_ROAD_TOP_L[1]), (2, EREZ_ROTEM_SIDEWK_TOP_R[1]-(ELLA_ROAD_TOP_L[1]))),
            # Bottom - Erez till Rotem
    pygame.Rect((EREZ_ROTEM_SIDEWK_TOP_R[0], EREZ_ROTEM_SIDEWK_TOP_R[1]), (2, EREZ_ROTEM_SIDEWK_TOP_R[1]+2*LANE_W-(EREZ_ROTEM_SIDEWK_TOP_R[1])))
    ]

YAAR_ROAD_BORDERS = [
    # Horizontal
        # Yaar Sidewalk bottom 
    pygame.Rect((YAAR_SIDEW_BOT_L[0], YAAR_SIDEW_BOT_L[1]), (YAAR_ROAD_MID_R[0]-1.1*LANE_W-(YAAR_SIDEW_BOT_L[0]), 2)),
            # Yaar Parallels top
    pygame.Rect((YAAR_ROAD_MID_R[0], SHAKED_SIDEWK_BOT_R[1]+4*LANE_W), (YAAR_ROAD_MID_R[0]+LANE_W-(YAAR_ROAD_MID_R[0]), 2)),
    # Vertical
            # Yaar Sidewalk left
    pygame.Rect((YAAR_SIDEW_BOT_L[0], EREZ_ROTEM_SIDEWK_TOP_R[1]), (2, YAAR_SIDEW_BOT_L[1]-(EREZ_ROTEM_SIDEWK_TOP_R[1]))),
            # Yaar Sidewalk right
    pygame.Rect((YAAR_ROAD_MID_R[0]-1.1*LANE_W, EREZ_ROTEM_SIDEWK_TOP_R[1]), (2, YAAR_SIDEW_BOT_L[1]-(EREZ_ROTEM_SIDEWK_TOP_R[1]))),
    
            # Yaar till Hadas (left)
    pygame.Rect((YAAR_ROAD_BOT_L[0], EREZ_ROTEM_SIDEWK_TOP_R[1]), (2, SHAKED_SIDEWK_BOT_R[1]-(EREZ_ROTEM_SIDEWK_TOP_R[1]))),
            # Yaar till Eshel
    pygame.Rect((YAAR_ROAD_BOT_L[0], ROTEM_ROAD_BOT_R[1]), (2, ESHEL_ROAD_BOT_R[1]-2*LANE_W-(ROTEM_ROAD_BOT_R[1]))),
    
            # Yaar till Rotem (right)
    pygame.Rect((YAAR_ROAD_MID_R[0], EREZ_ROTEM_SIDEWK_TOP_R[1]), (2, SHAKED_SIDEWK_BOT_R[1]-(EREZ_ROTEM_SIDEWK_TOP_R[1]))),
            # Yaar/Rotem till Parallels
    pygame.Rect((YAAR_ROAD_MID_R[0], ROTEM_ROAD_BOT_R[1]), (2, SHAKED_SIDEWK_BOT_R[1]+4*LANE_W-(ROTEM_ROAD_BOT_R[1]))),
            # Parallels (right)
    pygame.Rect((YAAR_ROAD_MID_R[0]+LANE_W, SHAKED_SIDEWK_BOT_R[1]+4*LANE_W), (2, ESHEL_ROAD_BOT_R[1]-(SHAKED_SIDEWK_BOT_R[1]+4*LANE_W)))
    ]

ELLA_ROAD_BORDERS = [
    # Vertical - left
        # Ella till Shaked
    pygame.Rect((ELLA_ROAD_TOP_L[0],ELLA_ROAD_TOP_L[1]), (2,SHAKED_SIDEWK_BOT_R[1]-(ELLA_ROAD_TOP_L[1]))),
        # Ella/Shaked till left PL
    pygame.Rect((ELLA_ROAD_TOP_L[0],ROTEM_ROAD_BOT_R[1]), (2,RBT_LEFT_CENTER[1]+3*LANE_W-(ROTEM_ROAD_BOT_R[1]))),
        # Ella left PL till Eshel
    pygame.Rect((ELLA_ROAD_TOP_L[0],RBT_LEFT_CENTER[1]+4.2*LANE_W), (2,ESHEL_ROAD_BOT_R[1]-2*LANE_W-(RBT_LEFT_CENTER[1]+4.2*LANE_W))),
    # Vertical - right
        # Ella till Shaked
    pygame.Rect((ELLA_ROAD_TOP_L[0]+LANE_W,EREZ_ROTEM_SIDEWK_TOP_R[1]), (2,SHAKED_SIDEWK_BOT_R[1]-(EREZ_ROTEM_SIDEWK_TOP_R[1]))),
        # Ella/Shaked till Eshel
    pygame.Rect((ELLA_ROAD_TOP_L[0]+LANE_W,ROTEM_ROAD_BOT_R[1]), (2,ESHEL_ROAD_BOT_R[1]-2*LANE_W-(ROTEM_ROAD_BOT_R[1])))
    ]

HADAS_ROAD_BORDERS = [
    # Vertical - left
        # Erez till Hadas
    pygame.Rect((MIRROR_CENTER/2,EREZ_ROTEM_SIDEWK_TOP_R[1]), (2, SHAKED_SIDEWK_BOT_R[1]-2.25*LANE_W-(EREZ_ROTEM_SIDEWK_TOP_R[1]))),
        # Hadas till Eshel
    pygame.Rect((MIRROR_CENTER/2,RBT_LEFT_CENTER[1]+3.25*LANE_W), (2, ESHEL_ROAD_BOT_R[1]-2*LANE_W-(RBT_LEFT_CENTER[1]+3.25*LANE_W))),
    # Vertical - right
        # Erez till Hadas
    pygame.Rect((MIRROR_CENTER/2+2*LANE_W,EREZ_ROTEM_SIDEWK_TOP_R[1]), (2, SHAKED_SIDEWK_BOT_R[1]-2.25*LANE_W-(EREZ_ROTEM_SIDEWK_TOP_R[1]))),
        # Hadas till Eshel
    pygame.Rect((MIRROR_CENTER/2+2*LANE_W,RBT_LEFT_CENTER[1]+3.25*LANE_W), (2, ESHEL_ROAD_BOT_R[1]-2*LANE_W-(RBT_LEFT_CENTER[1]+3.25*LANE_W)))
    ]

ROTEM_ROAD_BORDERS = [
    # Horizontal
        # Top
    pygame.Rect((YAAR_ROAD_MID_R[0], SHAKED_SIDEWK_BOT_R[1]), (RBT_RIGHT_CENTER[0]-1.5*LANE_W-(YAAR_ROAD_MID_R[0]), 2)),
        # Bottom - Yaar/Rotem till right PL
    pygame.Rect((YAAR_ROAD_MID_R[0], ROTEM_ROAD_BOT_R[1]), (EREZ_ROTEM_SIDEWK_TOP_R[0]+2*LANE_W-(YAAR_ROAD_MID_R[0]), 2)),
        # Bottom - right PL till Rotem
    pygame.Rect((EREZ_ROTEM_SIDEWK_TOP_R[0]+4.1*LANE_W, ROTEM_ROAD_BOT_R[1]), (ROTEM_ROAD_BOT_R[0]-(EREZ_ROTEM_SIDEWK_TOP_R[0]+4.1*LANE_W), 2)),        
    # Vertical
        # Left
    pygame.Rect((RBT_RIGHT_CENTER[0]-1.4*LANE_W,SHAKED_SIDEWK_BOT_R[1]-LANE_W), (2, (SHAKED_SIDEWK_BOT_R[1]+LANE_W)-SHAKED_SIDEWK_BOT_R[1])),
        # Right
    pygame.Rect((ROTEM_ROAD_BOT_R[0],ROTEM_ROAD_BOT_R[1]-3*LANE_W), (2, (ROTEM_ROAD_BOT_R[1]+3*LANE_W)-(ROTEM_ROAD_BOT_R[1])))
    ]

SHAKED_ROAD_BORDERS = [
    # Horizontal
        # Top
    pygame.Rect((0, SHAKED_SIDEWK_BOT_R[1]), (SHAKED_SIDEWK_BOT_R[0], 2)),
        # Bottom - till left pl
    pygame.Rect((0, SHAKED_SIDEWK_BOT_R[1]+2*LANE_W), (SHAKED_SIDEWK_BOT_R[0]/2+LANE_W, 2)),
        # Bottom - left pl till Ella
    pygame.Rect((SHAKED_SIDEWK_BOT_R[0]/2+2*LANE_W, SHAKED_SIDEWK_BOT_R[1]+2*LANE_W), (SHAKED_SIDEWK_BOT_R[0]-(SHAKED_SIDEWK_BOT_R[0]/2+2*LANE_W), 2)),
    ]

ESHEL_ROAD_BORDERS = [
    # Horizontal
        # Top - till left pl
    pygame.Rect((0, ESHEL_ROAD_BOT_R[1]-2*LANE_W), (SHAKED_SIDEWK_BOT_R[0]/2+LANE_W, 2)),
        # Top - left pl till Ella
    pygame.Rect((SHAKED_SIDEWK_BOT_R[0]/2+2*LANE_W, ESHEL_ROAD_BOT_R[1]-2*LANE_W), (SHAKED_SIDEWK_BOT_R[0]-(SHAKED_SIDEWK_BOT_R[0]/2+2*LANE_W), 2)),
        # Top - Ella till Hadas
    pygame.Rect((ELLA_ROAD_TOP_L[0]+LANE_W,ESHEL_ROAD_BOT_R[1]-2*LANE_W), (MIRROR_CENTER/2-(ELLA_ROAD_TOP_L[0]+LANE_W), 2)), 
        # Top - Hadas till Yaar
    pygame.Rect((MIRROR_CENTER/2+2*LANE_W,ESHEL_ROAD_BOT_R[1]-2*LANE_W), (YAAR_ROAD_BOT_L[0]-(MIRROR_CENTER/2+2*LANE_W), 2)), 
        # Bottom - Eshel till Parallels
    pygame.Rect((0,ESHEL_ROAD_BOT_R[1]), (2.1*LANE_W, 2)),
        # Bottom - Parallels
    pygame.Rect((2*LANE_W,ESHEL_ROAD_BOT_R[1]+LANE_W), (ELLA_ROAD_TOP_L[0]-(2*LANE_W), 2)),
        # Bottom - Parallels till Eshel/Yaar
    pygame.Rect((ELLA_ROAD_TOP_L[0],ESHEL_ROAD_BOT_R[1]), (ESHEL_ROAD_BOT_R[0]-(ELLA_ROAD_TOP_L[0]), 2)),
     # Vertical
        # Parallels - left
    pygame.Rect((2*LANE_W,ESHEL_ROAD_BOT_R[1]), (2, LANE_W)), 
        # Parallels - Right
    pygame.Rect((ELLA_ROAD_TOP_L[0],ESHEL_ROAD_BOT_R[1]), (2, LANE_W)) 
        
    ]

    # Parallel Parking Borders
YAAR_PP_BORDERS = [
    # Vertical
        # Top spot
    pygame.Rect((YAAR_ROAD_MID_R[0], ROTEM_ROAD_BOT_R[1]+2*LANE_W), (LANE_W, 2*LANE_W)),
        # Bottom spot
    pygame.Rect((YAAR_ROAD_MID_R[0], ROTEM_ROAD_BOT_R[1]+4.1*LANE_W), (LANE_W, 2*LANE_W))
    ]

ESHEL_PP_BORDERS = [
    # Horizontal
        # Left
    pygame.Rect((2.1*LANE_W, ESHEL_ROAD_BOT_R[1]), (2*LANE_W, LANE_W)),
        # Middle
    pygame.Rect((4.1*LANE_W, ESHEL_ROAD_BOT_R[1]), (2*LANE_W, LANE_W)),
        # Right
    pygame.Rect((6.1*LANE_W, ESHEL_ROAD_BOT_R[1]), (2*LANE_W, LANE_W))
    ]

    # Solid Lane borders
SOLID_LANE_BORDERS = [
    # Vertical - Erez
    pygame.Rect((YAAR_ROAD_BOT_L[0]+2.2*LANE_W,EREZ_ROTEM_SIDEWK_TOP_R[1]-LANE_W), (2, EREZ_ROTEM_SIDEWK_TOP_R[1]-(EREZ_ROTEM_SIDEWK_TOP_R[1]-LANE_W))),
    # Vertical - Yaar
    pygame.Rect((YAAR_ROAD_BOT_L[0]+2.2*LANE_W,YAAR_SIDEW_BOT_L[1]), (2, ESHEL_ROAD_BOT_R[1]-LANE_W-(YAAR_SIDEW_BOT_L[1]))),
    # Horizontal - Eshel
    pygame.Rect((YAAR_ROAD_BOT_L[0], ESHEL_ROAD_BOT_R[1]-1*LANE_W), (2*LANE_W, 2))
    ]
       
    # Lane Borders
EREZ_LANE_BORDERS = [
        # Horizontal - Top
    pygame.Rect((MIRROR_CENTER/3+LANE_W, HEIGHT/5.1), (EREZ_ROTEM_SIDEWK_TOP_R[0]-(MIRROR_CENTER/3), 2)),
        # Vertical - Erez/Rotem
    pygame.Rect((EREZ_ROTEM_SIDEWK_TOP_R[0]+LANE_W,EREZ_ROTEM_SIDEWK_TOP_R[1]-LANE_W), (2, EREZ_ROTEM_SIDEWK_TOP_R[1]+LANE_W-(EREZ_ROTEM_SIDEWK_TOP_R[1]-LANE_W))),       
        # Horizontal - Bottom - main sidewalk till right rbt
    pygame.Rect((EREZ_ROTEM_SIDEWK_TOP_R[0]+LANE_W, EREZ_ROTEM_SIDEWK_TOP_R[1]+LANE_W), (RBT_RIGHT_CENTER[0]-3.25*LANE_W-(EREZ_ROTEM_SIDEWK_TOP_R[0]+LANE_W), 2))
    ]

YAAR_LANE_BORDERS = [
        # Vertical - Middle of Left lanes
    pygame.Rect((YAAR_ROAD_BOT_L[0]+1.1*LANE_W,YAAR_SIDEW_BOT_L[1]), (2, (ESHEL_ROAD_BOT_R[1]-LANE_W)-(YAAR_SIDEW_BOT_L[1]))),      
        # Vertical - Middle of Right lanes
    pygame.Rect((YAAR_ROAD_MID_R[0]-1.1*LANE_W,YAAR_SIDEW_BOT_L[1]), (2, (ESHEL_ROAD_BOT_R[1]-LANE_W)-(YAAR_SIDEW_BOT_L[1])))
    ]

HADAS_LANE_BORDERS = [
    # Vertical
    pygame.Rect((MIRROR_CENTER/2+LANE_W,RBT_LEFT_CENTER[1]+3.2*LANE_W), (2, (ESHEL_ROAD_BOT_R[1]-2*LANE_W)-(RBT_LEFT_CENTER[1]+3.2*LANE_W)))    
    ]

ROTEM_LANE_BORDERS = [
    # Horizontal
    pygame.Rect((YAAR_ROAD_MID_R[0], SHAKED_SIDEWK_BOT_R[1]+LANE_W), (RBT_RIGHT_CENTER[0]-(YAAR_ROAD_MID_R[0]), 2))
    ]

SHAKED_LANE_BORDERS = [
    # Horizontal
    pygame.Rect((0, SHAKED_SIDEWK_BOT_R[1]+LANE_W), (SHAKED_SIDEWK_BOT_R[0], 2))
    ]

ESHEL_LANE_BORDERS = [
    # Horizontal
    pygame.Rect((0, ESHEL_ROAD_BOT_R[1]-LANE_W), (YAAR_ROAD_BOT_L[0], 2))
    ]    
#-------------------------------------------------------------------------
# Road Users Definitions 
#------------------------
RED_CAR = scale_image(pygame.image.load(DIR_IMGS + "Cars/red_car.png"), 0.28)

PLAYER_START_POS = (RBT_RIGHT_CENTER[0]+0.2*LANE_W,RBT_LEFT_CENTER[1]+2.5*LANE_W)

CAR_SCALE = 0.15
PED_SCALE = 0.85

YELLOW_CAR = scale_image(pygame.image.load(DIR_IMGS + "Cars/yellow_taxi.png"), CAR_SCALE)
BLUE_VAN = scale_image(pygame.image.load(DIR_IMGS + "Cars/blue_mini_truck.png"), CAR_SCALE)
WHITE_TRUCK = scale_image(pygame.image.load(DIR_IMGS + "Cars/white_truck.png"), CAR_SCALE)

RED_GIRL = scale_image(pygame.image.load(DIR_IMGS + "Peds/red_girl_small.png"), PED_SCALE)
GREEN_GIRL = scale_image(pygame.image.load(DIR_IMGS + "Peds/green_girl_small.png"), PED_SCALE)
OLD_MAN = scale_image(pygame.image.load(DIR_IMGS + "Peds/old_man_small.png"), PED_SCALE)
BLOND_BOY = scale_image(pygame.image.load(DIR_IMGS + "Peds/blond_boy_small.png"), PED_SCALE)

# Other Cars Paths (made using draw_points)
#-------------------------------------------
CAR_PATH_YAAR_TILL_LEFT_PL = [
    # Yaar
    (395, 215), (418, 309), 
    # Eshel
    (405, 415), (314, 399), 
    # Left PL
    (110, 399), (110, 300), (160, 300)] 
    
CAR_PATH_ESHEL_TILL_ROTEM = [
    # Eshel (left edge)
    (6, 425), (175, 425), (452, 422), 
    # Yaar
    (450, 270), 
    # Rotem (right edge)
    (774, 270)]

CAR_PATH_SHAKED_TILL_RIGHT_PL = [
    # Shaked (left edge)
    (6, 270), (200, 270), 
    # Left RBT
    (232, 282), (244, 308), (269, 326),
    (310, 314), (333, 295), (341, 271),
    # Yaar 
    (436, 270), (451, 246), (451, 174),
    # Erez
    (455, 117), (620, 117), (605, 182), 
    # Right RBT
    (692, 161), (705, 197), (742, 216), 
    # Rotem
    (742, 270), (671, 264),
    # Right PL (right edge) 
    (671, 333), (671, 386), (770, 378), (770, 425)
    ]

CAR_PATH_ROTEM_TILL_SHAKED = [
    # Rotem (right edge)
    (774, 270),  
    # Right RBT
    (772, 200), (807, 182), (817, 147),
    (800, 102), (753, 83), (710, 100), 
    (688, 140),
    # Erez
    (633, 140), (633, 85), (400, 90),
    # Ella
    (181, 90), (183, 127), (175, 258),
    # Shaked
    (6, 245)
    ]

# Pedestrians Paths (made using draw_points)
#-------------------------------------------
PED_PATH_ROTEM_SW_TILL_ELLA = [
    (500, 164), (470, 130), (425, 128), (395, 128),
    (369, 129), (335, 127), (307, 130), (287, 130), (262, 131),
    (231, 130), (203, 167), (174, 167), (144, 168), (101, 176),
    (47, 173), (22, 174)]

PED_PATH_YAAR_SW_TILL_RBT = [
    (587, 179), (630, 185), (671, 186), (702, 199),
    (737, 184), (764, 185), (794, 181), (822, 183), (841, 199)] 

PED_PATH_YAAR_SW_TILL_ROTEM_SW = [
    (552, 325), (523, 297), (516, 238), (535, 202)]

PED_PATH_ELLA_TILL_ESHEL = [
    (131, 163), (190, 230), (211, 288), (231, 360), (239, 422),
    (277, 457), (335, 460), (395, 457), (470,457)]
#-------------------------------------------------------------------------
# Car Directions Definitions
#---------------------------
DIRECTION_SMOOTH = 5

NORTH = 0
NORTH_WEST = 45
WEST = 90
SOUTH_WEST = 135
SOUTH = 180
SOUTH_EAST = 225
EAST = 270
NORTH_EAST = 315
#-------------------------------------------------------------------------
# Finish Line Definitions  
#------------------------
FINISH_LINE_HORI = stretch_image(pygame.image.load(DIR_IMGS + "Dashboard/finish_line.png"),0.5,0.7)
FINISH_LINE_VERT = pygame.transform.rotate(FINISH_LINE_HORI,90)

FINISH_LINE_PARKINGS = [
    # 4 - Left PL top left spot
    (EAST, PLS_RP_BORDERS[0]),

    # 7 - Eshel PP middle spot
    (EAST, ESHEL_PP_BORDERS[1]),

    # 9 - Yaar PP top spot
    (NORTH, YAAR_PP_BORDERS[0]),

    # 10 - Right PL bottom right spot
    (NORTH, PLS_RP_BORDERS[1]),
]

FINISH_LINE_IMGS = [
    # 1 - Exit right PL entering Rotem
    ("HORI", (EREZ_ROTEM_SIDEWK_TOP_R[0]+2*LANE_W, ROTEM_ROAD_BOT_R[1])),
    
    # 2 - Yaar after right turn from Rotem
    ("HORI", (YAAR_ROAD_MID_R[0]-2*LANE_W, YAAR_SIDEW_BOT_L[1]+2*LANE_W)),
    
    # 3 - Ella top after crosswalk
    ("HORI", (SHAKED_SIDEWK_BOT_R[0]-LANE_W, SHAKED_SIDEWK_BOT_R[1]+0.25*LANE_W)),
    
    # 4 - Left PL top left spot
    #(FINISH_LINE_HORI, (0.5*LANE_W, SHAKED_SIDEWK_BOT_R[1]+2.5*LANE_W)),
    ("PARKING", FINISH_LINE_PARKINGS[0][1]),

    # 5 - Erez entering right RBT
    ("VERT", (RBT_RIGHT_CENTER[0]-4.5*LANE_W, RBT_RIGHT_CENTER[1]-LANE_W)),
    
    # 6 - Yaar bottom before turn to Eshel
    ("HORI", (YAAR_ROAD_BOT_L[0], YAAR_ROAD_BOT_L[1])),
    
    # 7 - Eshel PP middle spot
    #(FINISH_LINE_HORI, (4.1*LANE_W, ESHEL_ROAD_BOT_R[1])),
    ("PARKING", FINISH_LINE_PARKINGS[1][1]),

    # 8 - Hadas RBT right exit
    ("VERT", (YAAR_ROAD_BOT_L[0], RBT_LEFT_CENTER[1]-LANE_W)),

    # 9 - Yaar PP top spot
    #(FINISH_LINE_VERT, (YAAR_ROAD_MID_R[0], ROTEM_ROAD_BOT_R[1]+2.1*LANE_W)),
    ("PARKING", FINISH_LINE_PARKINGS[2][1]),

    # 10 - Right PL bottom right spot
    #(FINISH_LINE_HORI, (ROTEM_ROAD_BOT_R[0]+2*LANE_W, ESHEL_ROAD_BOT_R[1]-1.5*LANE_W)),
    ("PARKING", FINISH_LINE_PARKINGS[3][1])]
#-------------------------------------------------------------------------
# Buildings Definitions  
#------------------------
RED_BLD = scale_image(pygame.image.load(DIR_IMGS + "Buildings/" + "tall_red_bld.png"), 0.15)
BLACK_BLD = scale_image(pygame.image.load(DIR_IMGS + "Buildings/" + "tall_black_bld.png"), 0.18)
PURPLE_BLD = scale_image(pygame.image.load(DIR_IMGS + "Buildings/" + "short_purple_bld.png"), 0.2)
BROWN_BLD = scale_image(pygame.image.load(DIR_IMGS + "Buildings/" + "short_brown_bld.png"), 0.25)

ROTEM_BLD_POS = (ROTEM_ROAD_BOT_R[0]+1.5*LANE_W, ROTEM_ROAD_BOT_R[1]-0.9*RED_BLD.get_height())
SHAKED_BLD_POS = (0, SHAKED_SIDEWK_BOT_R[1]-1.2*BLACK_BLD.get_height())
YAAR_BLD_TOP_POS = (YAAR_ROAD_MID_R[0]+0.5*LANE_W, EREZ_ROTEM_SIDEWK_TOP_R[1]+0.5*LANE_W)
YAAR_BLD_BOT_POS = (ESHEL_ROAD_BOT_R[0]-1*LANE_W, ESHEL_ROAD_BOT_R[1]-0.6*BROWN_BLD.get_height())
#-------------------------------------------------------------------------
# Levels Instructions Definitions  
#--------------------------------
LEVEL_1_INST = [ "You are in the red",
                "car, driving your mom",
                "for the first time since",
                "getting your license.",
                "(No pressure,right?)",
                "",
                "Exit the parking lot.",
                "Try not to hit a wall",
                "on your way out!",
                "If you do get stuck,",
                "try rotating the car",
                "while pressing W or S."]

LEVEL_2_INST = [ "Your mom asked you to",
                "give her a ride to work.",
                "",
                "Swing by the purple",
                "office building",
                "on HaYaar.",
                "",
                "Mind the pedestrians."]

LEVEL_3_INST = [ "Your friends called,",
                "they want to hang out",
                "at the mall.",
                "",
                "Get to the big mall",
                "via HaElla.",
                "",
                "Try not to drive",
                "against traffic."]

LEVEL_4_INST = [ "Underground parking",
                "lot is full.",
                "",
                "Park across the street.",
                "You'll get bonus points",
                "for parking in reverse!",
                "",
                "If you get stuck,",
                "try rotating the car",
                "while pressing W or S."]

LEVEL_5_INST = [ "You had a really",
                "good time!",
                "But your mom called,",
                "she forgot her lunch.",
                "",
                "Bring her some food",
                "to the Erez Park.",
                "",
                "Drive safely, try not",
                "to hit anything."]

LEVEL_6_INST = [ "Well done!",
                "But all of a sudden",
                "rain started pouring.",
                "",
                "You should get going.",
                "",
                "Don't forget to turn on",
                "the wipers!"]

LEVEL_7_INST = [ "Congratulations,",
                "your first flat tire!",
                "",
                "Keep going down Eshel,",
                "you can stop and",
                "change your tire there.",
                "",
                "Don't forget to park!"]

LEVEL_8_INST = [ "Looking good!",
                "But you decided to test",
                "the tires in a roundabout",
                "just to make sure.",
                "",
                "Try not to drive",
                "into other cars or",
                "pedestrians."]

LEVEL_9_INST = [ "Tires are fine, but",
                "your little brother and",
                "sister called, asking",
                "you to pick them up",
                "from the library.",
                "They stayed late",
                "working on a project.",
                "",
                "Park next to it on Yaar.",
                "",
                "Don't forget to turn",
                "on the lights!"]

LEVEL_10_INST = [ "Wow, has it been a",
                "whole day already?",
                "",
                "Let's drive back home!",
                "",
                "You got this, you're a",
                "pro by now :)"]

LEVELS_INSTS = [LEVEL_1_INST, LEVEL_2_INST, 
                LEVEL_3_INST, LEVEL_4_INST, 
                LEVEL_5_INST, LEVEL_6_INST,
                LEVEL_7_INST, LEVEL_8_INST,
                LEVEL_9_INST, LEVEL_10_INST]
#-------------------------------------------------------------------------
# Functions (called by the main program)
#---------------------------------------
def draw_buildings():
    """
    Draw all the buildings
    """
    BUILDINGS = [(RED_BLD, ROTEM_BLD_POS),
                (BLACK_BLD,SHAKED_BLD_POS),
                (PURPLE_BLD,YAAR_BLD_TOP_POS),
                (BROWN_BLD,YAAR_BLD_BOT_POS)]

    for building, pos in BUILDINGS:
        WIN.blit(building, pos)  

def draw_street_names():
    """
    Draw all the street names 
    """
    STREETS = [ ("HaErez", (RBT_LEFT_CENTER[0]-2*LANE_W,EREZ_ROTEM_SIDEWK_TOP_R[1]-2*LANE_W)),
                ("HaErez", (YAAR_ROAD_MID_R[0],EREZ_ROTEM_SIDEWK_TOP_R[1]-LANE_W)),
                ("HaHadas", (RBT_LEFT_CENTER[0]-2.2*LANE_W,EREZ_ROTEM_SIDEWK_TOP_R[1]+3*LANE_W)), 
                ("HaRotem", (RBT_RIGHT_CENTER[0]-2.5*LANE_W,EREZ_ROTEM_SIDEWK_TOP_R[1]+3*LANE_W)),
                ("HaRotem", (EREZ_ROTEM_SIDEWK_TOP_R[0]+1.5*LANE_W,RBT_LEFT_CENTER[1])),
                ("HaYaar", (YAAR_ROAD_MID_R[0]-4*LANE_W,RBT_LEFT_CENTER[1]-LANE_W)),
                ("HaElla", (SHAKED_SIDEWK_BOT_R[0],SHAKED_SIDEWK_BOT_R[1]-2.5*LANE_W)),
                ("HaElla", (SHAKED_SIDEWK_BOT_R[0],SHAKED_SIDEWK_BOT_R[1]+LANE_W)),
                ("HaShaked",(0,RBT_LEFT_CENTER[1])),
                ("HaEshel", (SHAKED_SIDEWK_BOT_R[0]-2*LANE_W,DASHBOARD_HOR_TOP-4*LANE_W))]
    
    for streetName, pos in STREETS:
        street_text = STREETS_FONT.render(streetName,1,PINK)
        if streetName == "HaElla":
            # rotate the text from horizontal to vertical
            street_text = pygame.transform.rotate(street_text,90)
            
        street_text_pos = (pos[0]+street_text.get_rect().centerx, pos[1]+street_text.get_rect().centery)
        WIN.blit(street_text, street_text_pos)  

#-------------------------------------------------------------------------
# Helper Functions (called by the main program at dev stage only)
#----------------------------------------------------------------
def draw_borders():
    """
    Draw the scene borders (roads, lanes, parallel parking spots)
    """
    def draw_road_borders():

        for r in EREZ_ROAD_BORDERS:
            pygame.draw.rect(WIN, BLUE, r)
        
        for r in YAAR_ROAD_BORDERS:
            pygame.draw.rect(WIN, BLUE, r)

        for r in ELLA_ROAD_BORDERS:
            pygame.draw.rect(WIN, BLUE, r)

        for r in HADAS_ROAD_BORDERS:
            pygame.draw.rect(WIN, BLUE, r)

        for r in ROTEM_ROAD_BORDERS:
            pygame.draw.rect(WIN, BLUE, r)
        
        for r in SHAKED_ROAD_BORDERS:
            pygame.draw.rect(WIN, BLUE, r)

        for r in ESHEL_ROAD_BORDERS:
            pygame.draw.rect(WIN, BLUE, r)
        
        """
            # Erez - Top Road 
            # Horizontal
                # Top (border with sky)
        pygame.draw.line(WIN, RED, (MIRROR_CENTER/3, ELLA_ROAD_TOP_L[1]), (EREZ_ROTEM_SIDEWK_TOP_R[0]+2*LANE_W, ELLA_ROAD_TOP_L[1]), 1)
                # Top (border with park)
        pygame.draw.line(WIN, RED, (EREZ_ROTEM_SIDEWK_TOP_R[0]+2*LANE_W, EREZ_ROTEM_SIDEWK_TOP_R[1]), (RBT_RIGHT_CENTER[0]-3.25*LANE_W, EREZ_ROTEM_SIDEWK_TOP_R[1]), 1)
                # Bottom - Ella till Hadas
        pygame.draw.line(WIN, RED, (MIRROR_CENTER/3+LANE_W, EREZ_ROTEM_SIDEWK_TOP_R[1]), (MIRROR_CENTER/2, EREZ_ROTEM_SIDEWK_TOP_R[1]), 1)
                # Bottom - Hadas till Yaar
        pygame.draw.line(WIN, RED, (MIRROR_CENTER/2+2*LANE_W+2, EREZ_ROTEM_SIDEWK_TOP_R[1]), (YAAR_ROAD_BOT_L[0], EREZ_ROTEM_SIDEWK_TOP_R[1]), 1)
                # Bottom - Yaar Sidewalk
        pygame.draw.line(WIN, RED, (YAAR_SIDEW_BOT_L[0], EREZ_ROTEM_SIDEWK_TOP_R[1]), (YAAR_ROAD_MID_R[0]-1.1*LANE_W, EREZ_ROTEM_SIDEWK_TOP_R[1]), 1)
                # Bottom - Yaar till Erez 
        pygame.draw.line(WIN, RED, (YAAR_ROAD_MID_R[0], EREZ_ROTEM_SIDEWK_TOP_R[1]), (EREZ_ROTEM_SIDEWK_TOP_R[0], EREZ_ROTEM_SIDEWK_TOP_R[1]), 1)
                # Bottom - Erez till Rotem
        pygame.draw.line(WIN, RED, (EREZ_ROTEM_SIDEWK_TOP_R[0], EREZ_ROTEM_SIDEWK_TOP_R[1]+2*LANE_W), (RBT_RIGHT_CENTER[0]-3.25*LANE_W, EREZ_ROTEM_SIDEWK_TOP_R[1]+2*LANE_W), 1)
            # Vertical
                # Top - Erez till Rotem
        pygame.draw.line(WIN, RED, (EREZ_ROTEM_SIDEWK_TOP_R[0]+2*LANE_W, ELLA_ROAD_TOP_L[1]), (EREZ_ROTEM_SIDEWK_TOP_R[0]+2*LANE_W,EREZ_ROTEM_SIDEWK_TOP_R[1]), 1)
                # Bottom - Erez till Rotem
        pygame.draw.line(WIN, RED, (EREZ_ROTEM_SIDEWK_TOP_R[0], EREZ_ROTEM_SIDEWK_TOP_R[1]), (EREZ_ROTEM_SIDEWK_TOP_R[0],EREZ_ROTEM_SIDEWK_TOP_R[1]+2*LANE_W), 1)
        

            # Yaar - Main Road
            # Horizontal
                # Yaar Sidewalk bottom 
        pygame.draw.line(WIN, RED, (YAAR_SIDEW_BOT_L[0], YAAR_SIDEW_BOT_L[1]), (YAAR_ROAD_MID_R[0]-1.1*LANE_W, YAAR_SIDEW_BOT_L[1]), 1)
                # Yaar Parallels top
        pygame.draw.line(WIN, RED, (YAAR_ROAD_MID_R[0], SHAKED_SIDEWK_BOT_R[1]+4*LANE_W), (YAAR_ROAD_MID_R[0]+LANE_W, SHAKED_SIDEWK_BOT_R[1]+4*LANE_W), 1)
            # Vertical
                # Yaar Sidewalk left
        pygame.draw.line(WIN, RED, (YAAR_SIDEW_BOT_L[0], EREZ_ROTEM_SIDEWK_TOP_R[1]), (YAAR_SIDEW_BOT_L[0], YAAR_SIDEW_BOT_L[1]), 1)
                # Yaar Sidewalk right
        pygame.draw.line(WIN, RED, (YAAR_ROAD_MID_R[0]-1.1*LANE_W, EREZ_ROTEM_SIDEWK_TOP_R[1]), (YAAR_ROAD_MID_R[0]-1.1*LANE_W, YAAR_SIDEW_BOT_L[1]), 1)
        
                # Yaar till Hadas (left)
        pygame.draw.line(WIN, RED, (YAAR_ROAD_BOT_L[0], EREZ_ROTEM_SIDEWK_TOP_R[1]), (YAAR_ROAD_BOT_L[0], SHAKED_SIDEWK_BOT_R[1]), 1)
                # Yaar till Eshel
        pygame.draw.line(WIN, RED, (YAAR_ROAD_BOT_L[0], ROTEM_ROAD_BOT_R[1]), (YAAR_ROAD_BOT_L[0], ESHEL_ROAD_BOT_R[1]-2*LANE_W), 1)
        
                # Yaar till Rotem (right)
        pygame.draw.line(WIN, RED, (YAAR_ROAD_MID_R[0], EREZ_ROTEM_SIDEWK_TOP_R[1]), (YAAR_ROAD_MID_R[0], SHAKED_SIDEWK_BOT_R[1]), 1)
                # Yaar/Rotem till Parallels
        pygame.draw.line(WIN, RED, (YAAR_ROAD_MID_R[0], ROTEM_ROAD_BOT_R[1]), (YAAR_ROAD_MID_R[0], SHAKED_SIDEWK_BOT_R[1]+4*LANE_W), 1)
                # Parallels (right)
        pygame.draw.line(WIN, RED, (YAAR_ROAD_MID_R[0]+LANE_W, SHAKED_SIDEWK_BOT_R[1]+4*LANE_W), (YAAR_ROAD_MID_R[0]+LANE_W, ESHEL_ROAD_BOT_R[1]), 1)
        
        
        # Ella - One Way Road
        # Vertical - left
            # Ella till Shaked
        pygame.draw.line(WIN, RED, (ELLA_ROAD_TOP_L[0],ELLA_ROAD_TOP_L[1]), (ELLA_ROAD_TOP_L[0],SHAKED_SIDEWK_BOT_R[1]), 1)
            # Ella/Shaked till left PL
        #pygame.draw.line(WIN, RED, (ELLA_ROAD_TOP_L[0],ROTEM_ROAD_BOT_R[1]), (ELLA_ROAD_TOP_L[0],RBT_LEFT_CENTER[1]+3*LANE_W), 1)
            # Ella left PL till Eshel
        #pygame.draw.line(WIN, RED, (ELLA_ROAD_TOP_L[0],RBT_LEFT_CENTER[1]+4.2*LANE_W), (ELLA_ROAD_TOP_L[0],ESHEL_ROAD_BOT_R[1]-2*LANE_W), 1)
        # Vertical - right
            # Ella till Shaked
        pygame.draw.line(WIN, RED, (ELLA_ROAD_TOP_L[0]+LANE_W,EREZ_ROTEM_SIDEWK_TOP_R[1]), (ELLA_ROAD_TOP_L[0]+LANE_W,SHAKED_SIDEWK_BOT_R[1]), 1)
            # Ella/Shaked till Eshel
        pygame.draw.line(WIN, RED, (ELLA_ROAD_TOP_L[0]+LANE_W,ROTEM_ROAD_BOT_R[1]), (ELLA_ROAD_TOP_L[0]+LANE_W,ESHEL_ROAD_BOT_R[1]-2*LANE_W), 1)
        
        
        # Hadas
        # Vertical - left
            # Erez till Hadas
        pygame.draw.line(WIN, RED, (MIRROR_CENTER/2,EREZ_ROTEM_SIDEWK_TOP_R[1]), (MIRROR_CENTER/2, SHAKED_SIDEWK_BOT_R[1]-2.25*LANE_W), 1)
            # Hadas till Eshel
        pygame.draw.line(WIN, RED, (MIRROR_CENTER/2,RBT_LEFT_CENTER[1]+3.25*LANE_W), (MIRROR_CENTER/2, ESHEL_ROAD_BOT_R[1]-2*LANE_W), 1)
        # Vertical - right
            # Erez till Hadas
        pygame.draw.line(WIN, RED, (MIRROR_CENTER/2+2*LANE_W,EREZ_ROTEM_SIDEWK_TOP_R[1]), (MIRROR_CENTER/2+2*LANE_W, SHAKED_SIDEWK_BOT_R[1]-2.25*LANE_W), 1)
            # Hadas till Eshel
        pygame.draw.line(WIN, RED, (MIRROR_CENTER/2+2*LANE_W,RBT_LEFT_CENTER[1]+3.25*LANE_W), (MIRROR_CENTER/2+2*LANE_W, ESHEL_ROAD_BOT_R[1]-2*LANE_W), 1)
        
        
        # Rotem
        # Horizontal
            # Top
        pygame.draw.line(WIN, RED, (YAAR_ROAD_MID_R[0], SHAKED_SIDEWK_BOT_R[1]), (RBT_RIGHT_CENTER[0]-1.5*LANE_W, SHAKED_SIDEWK_BOT_R[1]), 1)
            # Bottom - Yaar/Rotem till right PL
        pygame.draw.line(WIN, RED, (YAAR_ROAD_MID_R[0], ROTEM_ROAD_BOT_R[1]), (EREZ_ROTEM_SIDEWK_TOP_R[0]+2*LANE_W, ROTEM_ROAD_BOT_R[1]), 1)
            # Bottom - right PL till Rotem
        pygame.draw.line(WIN, RED, (EREZ_ROTEM_SIDEWK_TOP_R[0]+4.1*LANE_W, ROTEM_ROAD_BOT_R[1]), (ROTEM_ROAD_BOT_R[0], ROTEM_ROAD_BOT_R[1]), 1)
        # Vertical
            # Left
        pygame.draw.line(WIN, RED, (RBT_RIGHT_CENTER[0]-1.4*LANE_W,SHAKED_SIDEWK_BOT_R[1]), (RBT_RIGHT_CENTER[0]-1.4*LANE_W, SHAKED_SIDEWK_BOT_R[1]-LANE_W), 1)
            # Right
        pygame.draw.line(WIN, RED, (ROTEM_ROAD_BOT_R[0],ROTEM_ROAD_BOT_R[1]), (ROTEM_ROAD_BOT_R[0], SHAKED_SIDEWK_BOT_R[1]-LANE_W), 1)
        

        # Shaked - Horizontal
        pygame.draw.line(WIN, RED, (0, SHAKED_SIDEWK_BOT_R[1]), (SHAKED_SIDEWK_BOT_R[0], SHAKED_SIDEWK_BOT_R[1]), 1)
        

        # Eshel
        # Horizontal
            # Top - Ella till Hadas
        pygame.draw.line(WIN, RED, (ELLA_ROAD_TOP_L[0]+LANE_W,ESHEL_ROAD_BOT_R[1]-2*LANE_W), (MIRROR_CENTER/2, ESHEL_ROAD_BOT_R[1]-2*LANE_W), 1) 
            # Top - Hadas till Yaar
        pygame.draw.line(WIN, RED, (MIRROR_CENTER/2+2*LANE_W,ESHEL_ROAD_BOT_R[1]-2*LANE_W), (YAAR_ROAD_BOT_L[0], ESHEL_ROAD_BOT_R[1]-2*LANE_W), 1) 
            # Bottom - Eshel till Parallels
        pygame.draw.line(WIN, RED, (0,ESHEL_ROAD_BOT_R[1]), (2.1*LANE_W, ESHEL_ROAD_BOT_R[1]), 1)
            # Bottom - Parallels
        pygame.draw.line(WIN, RED, (2*LANE_W,ESHEL_ROAD_BOT_R[1]+LANE_W), (ELLA_ROAD_TOP_L[0], ESHEL_ROAD_BOT_R[1]+LANE_W), 1)
            # Bottom - Parallels till Eshel/Yaar
        pygame.draw.line(WIN, RED, (ELLA_ROAD_TOP_L[0],ESHEL_ROAD_BOT_R[1]), (ESHEL_ROAD_BOT_R[0], ESHEL_ROAD_BOT_R[1]), 1) 
        # Vertical
            # Parallels - left
        pygame.draw.line(WIN, RED, (2*LANE_W,ESHEL_ROAD_BOT_R[1]), (2*LANE_W, ESHEL_ROAD_BOT_R[1]+LANE_W), 1) 
            # Parallels - Right
        pygame.draw.line(WIN, RED, (ELLA_ROAD_TOP_L[0],ESHEL_ROAD_BOT_R[1]), (ELLA_ROAD_TOP_L[0], ESHEL_ROAD_BOT_R[1]+LANE_W), 1) 
        """

            # Roundabouts - outer ring
        pygame.draw.circle(WIN,RED,RBT_LEFT_CENTER,RADIUS+1.5*LANE_W,1)
        pygame.draw.circle(WIN,RED,RBT_RIGHT_CENTER,RADIUS+1.5*LANE_W,1)
            # Roundabouts - inner ring
        pygame.draw.circle(WIN,RED,RBT_LEFT_CENTER,RADIUS-1.3*LANE_W,1)
        pygame.draw.circle(WIN,RED,RBT_RIGHT_CENTER,RADIUS-1.3*LANE_W,1)

    def draw_lane_borders():

        for r in SOLID_LANE_BORDERS:
            pygame.draw.rect(WIN, RED, r)

        for r in EREZ_LANE_BORDERS:
            pygame.draw.rect(WIN, GREEN, r)
        
        for r in YAAR_LANE_BORDERS:
            pygame.draw.rect(WIN, GREEN, r)

        for r in HADAS_LANE_BORDERS:
            pygame.draw.rect(WIN, GREEN, r)

        for r in ROTEM_LANE_BORDERS:
            pygame.draw.rect(WIN, GREEN, r)

        for r in SHAKED_LANE_BORDERS:
            pygame.draw.rect(WIN, GREEN, r)
        
        for r in ESHEL_LANE_BORDERS:
            pygame.draw.rect(WIN, GREEN, r)

        """
            # Erez
                # Horizontal - Top
        pygame.draw.line(WIN, GREEN, (MIRROR_CENTER/3+LANE_W, HEIGHT/5.1), (EREZ_ROTEM_SIDEWK_TOP_R[0]+LANE_W, HEIGHT/5.1), 1) 
                # Horizontal - Bottom - main sidewalk till right rbt
        pygame.draw.line(WIN, GREEN, (EREZ_ROTEM_SIDEWK_TOP_R[0]+LANE_W, EREZ_ROTEM_SIDEWK_TOP_R[1]+LANE_W), (RBT_RIGHT_CENTER[0], EREZ_ROTEM_SIDEWK_TOP_R[1]+LANE_W), 1)
                # Vertical - Solid lane line
        pygame.draw.line(WIN, RED, (YAAR_ROAD_BOT_L[0]+2.2*LANE_W, EREZ_ROTEM_SIDEWK_TOP_R[1]-LANE_W), (YAAR_ROAD_BOT_L[0]+2.2*LANE_W, EREZ_ROTEM_SIDEWK_TOP_R[1]), 1)
                # Vertical - Erez/Rotem
        pygame.draw.line(WIN, GREEN, (EREZ_ROTEM_SIDEWK_TOP_R[0]+LANE_W, EREZ_ROTEM_SIDEWK_TOP_R[1]-LANE_W), (EREZ_ROTEM_SIDEWK_TOP_R[0]+LANE_W, EREZ_ROTEM_SIDEWK_TOP_R[1]+LANE_W), 1)
        

            # Yaar - Vertical
                # Left Lane Line
        #pygame.draw.line(WIN, GREEN, (YAAR_ROAD_BOT_L[0]+1.1*LANE_W, YAAR_SIDEW_BOT_L[1]), (YAAR_ROAD_BOT_L[0]+1.1*LANE_W, ESHEL_ROAD_BOT_R[1]-LANE_W), 1)
                # Solid Lane Line
        pygame.draw.line(WIN, RED, (YAAR_ROAD_BOT_L[0]+2.2*LANE_W, YAAR_SIDEW_BOT_L[1]), (YAAR_ROAD_BOT_L[0]+2.2*LANE_W, ESHEL_ROAD_BOT_R[1]-LANE_W), 1)
                # Right Lane Line
        pygame.draw.line(WIN, GREEN, (YAAR_ROAD_MID_R[0]-LANE_W, YAAR_SIDEW_BOT_L[1]), (YAAR_ROAD_MID_R[0]-LANE_W, ESHEL_ROAD_BOT_R[1]-LANE_W), 1)
        

            # Hadas - Vertical
        pygame.draw.line(WIN, GREEN, (MIRROR_CENTER/2+LANE_W, RBT_LEFT_CENTER[1]+3.2*LANE_W), (MIRROR_CENTER/2+LANE_W, ESHEL_ROAD_BOT_R[1]-2*LANE_W), 1)
        

            # Rotem - Horizontal
        pygame.draw.line(WIN, GREEN, (YAAR_ROAD_MID_R[0], SHAKED_SIDEWK_BOT_R[1]+LANE_W), (RBT_RIGHT_CENTER[0], SHAKED_SIDEWK_BOT_R[1]+LANE_W), 1)
        

            # Shaked - Horizontal
        pygame.draw.line(WIN, GREEN, (0, SHAKED_SIDEWK_BOT_R[1]+LANE_W), (SHAKED_SIDEWK_BOT_R[0], SHAKED_SIDEWK_BOT_R[1]+LANE_W), 1)
        

            # Eshel - Horizontal
                # Dashed
        pygame.draw.line(WIN, GREEN, (0,ESHEL_ROAD_BOT_R[1]-LANE_W), (YAAR_ROAD_BOT_L[0], ESHEL_ROAD_BOT_R[1]-LANE_W), 1) 
                # Solid
        pygame.draw.line(WIN, RED, (YAAR_ROAD_BOT_L[0],ESHEL_ROAD_BOT_R[1]-0.8*LANE_W), (YAAR_ROAD_BOT_L[0]+2*LANE_W, ESHEL_ROAD_BOT_R[1]-0.8*LANE_W), 1) 
        """
            # Roundabouts
        pygame.draw.circle(WIN,GREEN,RBT_LEFT_CENTER,RADIUS,1)
        pygame.draw.circle(WIN,GREEN,RBT_RIGHT_CENTER,RADIUS,1)
    
    def draw_parallel_parking_borders():

        for r in YAAR_PP_BORDERS:
            pygame.draw.rect(WIN, ORANGE, r)

        for r in ESHEL_PP_BORDERS:
            pygame.draw.rect(WIN, ORANGE, r)

        """
        # Yaar - Horizontal
            # Top spot
        pygame.draw.line(WIN, BLUE, (YAAR_ROAD_MID_R[0], ROTEM_ROAD_BOT_R[1]+4*LANE_W), (YAAR_ROAD_MID_R[0]+LANE_W, ROTEM_ROAD_BOT_R[1]+4*LANE_W), 1)
            # Bottom spot
        pygame.draw.line(WIN, BLUE, (YAAR_ROAD_MID_R[0], ESHEL_ROAD_BOT_R[1]-LANE_W), (YAAR_ROAD_MID_R[0]+LANE_W, ESHEL_ROAD_BOT_R[1]-LANE_W), 1)


        # Eshel - Vertical
            # Left
        pygame.draw.line(WIN, BLUE, (4.1*LANE_W,ESHEL_ROAD_BOT_R[1]), (4.1*LANE_W, ESHEL_ROAD_BOT_R[1]+LANE_W), 1) 
            # Right
        pygame.draw.line(WIN, BLUE, (6.1*LANE_W,ESHEL_ROAD_BOT_R[1]), (6.1*LANE_W, ESHEL_ROAD_BOT_R[1]+LANE_W), 1) 
        """

    draw_road_borders()
    draw_lane_borders()
    draw_parallel_parking_borders()

def draw_finish_lines():
    """
    Draw all the finish lines
    """
    for img, pos in FINISH_LINE_IMGS:
        if img == "HORI":
            WIN.blit(FINISH_LINE_HORI, pos)
        elif img == "VERT":
            WIN.blit(FINISH_LINE_VERT,pos)
        else:
            pygame.draw.rect(WIN, ORANGE, pos)

def draw_masks():
    #pygame.draw.rect(WIN,RED,LEFT_PL_BORDER_RECT,5)
    #pygame.draw.rect(WIN,RED,RIGHT_PL_BORDER_RECT,5)

    for m in MASKS_IMGS:
        WIN.blit(m, (0,SCENE_HEIGHT_START))

def print_all_possible_fonts():
    print(*pygame.font.get_fonts(), sep = "\n")        