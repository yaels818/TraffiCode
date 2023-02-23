# Outsource Imports
import pygame
import os

# Local Imports
from utils import scale_image, stretch_image

def load_button_images():
    
    BTNS_PATH = "Assets\Images\Dashboard\Buttons/"
    for i in range(1,7):
        image_off = pygame.image.load(BTNS_PATH + "OFF/btn" + str(i) + ".png")
        image_on = pygame.image.load(BTNS_PATH + "ON/btn" + str(i) + ".png")
        BTN_IMGS_OFF.append(image_off)
        BTN_IMGS_ON.append(image_on)

#-------------------------------------------------------------------------
# Screen Definitions
WIDTH, HEIGHT = 1200, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.display.set_caption("TraffiCode")
pygame.display.set_icon(scale_image(pygame.image.load("Assets\Images\gameIcon.png"),0.2))
#-------------------------------------------------------------------------
# Font Definitions
pygame.font.init()
MAIN_FONT = pygame.font.SysFont("centurygothic", 36)
DASH_FONT = pygame.font.SysFont("erasdemiitc", 26)
CLIP_FONT = pygame.font.SysFont("erasdemiitc", 19)
STREETS_FONT = pygame.font.SysFont("erasdemiitc", 12)
#-------------------------------------------------------------------------
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
ORANGE = (255,127,39)
#-------------------------------------------------------------------------
# Position Markers - center x
SCENE_HEIGHT_START = HEIGHT/12
SCENE_CENTER = (WIDTH - WIDTH/4.7)/2
MIRROR_CENTER = (WIDTH/2 + (WIDTH - WIDTH/4.7)/2)/2
DASHBOARD_HOR_TOP = HEIGHT-HEIGHT/7
DASHBOARD_VERT_LEFT = WIDTH - WIDTH/4.5
CLIP_LEFT = WIDTH - WIDTH/4.7
CLIP_CENTER = WIDTH - WIDTH/8.5 
CLIP_TOP = HEIGHT/7.5
LIGHTS_BTN_CENTER = WIDTH-CLIP_CENTER
#-------------------------------------------------------------------------

PATH = "Assets\Images/"

# Asset Definitions - Scene
SKY_DAY = scale_image(pygame.image.load(PATH + "Backgrounds/" + "day_sky.jpg"),0.25)
SKY_NIGHT = scale_image(pygame.image.load(PATH + "Backgrounds/" + "night_sky.jpg"),0.5)
SKY_RAINY = scale_image(pygame.image.load(PATH + "Backgrounds/" + "rainy_sky.jpg"),0.3)
SKY_SUNNY = scale_image(pygame.image.load(PATH + "Backgrounds/" + "sunny_sky.jpg"),0.25)

SCENE = scale_image(pygame.image.load(PATH + "Scenes\scene_1_light.png"),1.4)
SCENE_DARK = scale_image(pygame.image.load(PATH + "Scenes\scene_1_dark.png"),1.4)
LEVEL_IMGS = [(SKY_DAY, (0,0)), (SCENE, (0, SCENE_HEIGHT_START))]

# Asset Definitions - Scene Masks
BORDER_LEFT_PL = scale_image(pygame.image.load(PATH + "Borders\Scene_1/" + "mask_left_pl_bw_wider.png"),1.4)
BORDER_LEFT_RBT = scale_image(pygame.image.load(PATH + "Borders\Scene_1/" + "mask_left_rbt_bw.png"),1.4)
BORDER_RIGHT_PL = scale_image(pygame.image.load(PATH + "Borders\Scene_1/" + "mask_right_pl_bw.png"),1.4)
BORDER_RIGHT_RBT = scale_image(pygame.image.load(PATH + "Borders\Scene_1/" + "mask_right_rbt_bw.png"),1.4)

MASK_LEFT_PL = pygame.mask.from_surface(BORDER_LEFT_PL)
MASK_LEFT_RBT = pygame.mask.from_surface(BORDER_LEFT_RBT)
MASK_RIGHT_PL = pygame.mask.from_surface(BORDER_RIGHT_PL)
MASK_RIGHT_RBT = pygame.mask.from_surface(BORDER_RIGHT_RBT)

#-------------------------------------------------------------------------
DASHBOARD_RECT_HOR = pygame.Rect(0, DASHBOARD_HOR_TOP, WIDTH,HEIGHT/4)
DASHBOARD_RECT_VER = pygame.Rect(WIDTH - WIDTH/4.5, 0, WIDTH/4, HEIGHT) 
SPEEDOMETER = scale_image(pygame.image.load(PATH + "Dashboard/speedometer.png"),0.3)
MIRROR = scale_image(pygame.image.load(PATH + "Dashboard/rear_view_mirror.png"),0.25)
CLIPBOARD = stretch_image(pygame.image.load(PATH + "Dashboard/clipboard.png"),0.55,0.8)

# Position Definitions - center
SPEEDOMETER_POS = (MIRROR_CENTER-SPEEDOMETER.get_rect().centerx, DASHBOARD_HOR_TOP-SPEEDOMETER.get_rect().centery/2)
MIRROR_POS = (MIRROR_CENTER-MIRROR.get_rect().centerx, MIRROR.get_rect().centery/3)
CLIP_POS = (CLIP_CENTER-CLIPBOARD.get_rect().centerx,CLIP_TOP-CLIPBOARD.get_rect().centery/2.5)

DASH_IMGS = [(SPEEDOMETER, SPEEDOMETER_POS), (MIRROR, MIRROR_POS),(CLIPBOARD, CLIP_POS)]

#-------------------------------------------------------------------------
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
WIPERS_BTN_POS = (RIGHT_BLINK_POS[0]+BTN_IMGS_OFF[3].get_rect().centerx*1.5, DASHBOARD_HOR_TOP)
AC_BTN_POS = (WIPERS_BTN_POS[0]+BTN_IMGS_OFF[4].get_rect().centerx, DASHBOARD_HOR_TOP)
MUSIC_BTN_POS = (CLIP_CENTER-BTN_IMGS_OFF[5].get_rect().centerx/2, DASHBOARD_HOR_TOP)

# Buttons Blueprints for DashboardButton
MENU_BTN_BLP = [MENU_BTN_IMG,MENU_BTN_IMG,BTN_SCALE,*MENU_BTN_POS]
LIGHTS_BTN_BLP = [BTN_IMGS_OFF[0],BTN_IMGS_ON[0],BTN_SCALE,*LIGHTS_BTN_POS]
LEFT_BLINK_BLP = [BTN_IMGS_OFF[1],BTN_IMGS_ON[1],BLINKER_SCALE,*LEFT_BLINK_POS]
RIGHT_BLINK_BLP = [BTN_IMGS_OFF[2],BTN_IMGS_ON[2],BLINKER_SCALE,*RIGHT_BLINK_POS]
WIPERS_BTN_BLP = [BTN_IMGS_OFF[3],BTN_IMGS_ON[3],BTN_SCALE,*WIPERS_BTN_POS]
AC_BTN_BLP = [BTN_IMGS_OFF[4],BTN_IMGS_ON[4],BTN_SCALE,*AC_BTN_POS]
MUSIC_BTN_BLP = [BTN_IMGS_OFF[5],BTN_IMGS_ON[5],BTN_SCALE,*MUSIC_BTN_POS]

SPEEDOMETER_TEXT_POS = (MIRROR_CENTER,SPEEDOMETER_POS[1]+SPEEDOMETER.get_rect().centery)
#-------------------------------------------------------------------------

# Road Users Definitions 
RED_CAR = scale_image(pygame.image.load(PATH + "Cars/red_car.png"), 0.27)
#-------------------------------------------------------------------------
# Road Definitions
LANE_W = 22 # Lane Width in px

YAAR_ROAD_BOT_L = (LEFT_BLINK_POS[0] + BTN_IMGS_OFF[1].get_rect().centerx/2, HEIGHT-HEIGHT/3+5)
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
LEFT_PL_BORDER_RECT = pygame.Rect((0, SHAKED_SIDEWK_BOT_R[1]+2*LANE_W), (SHAKED_SIDEWK_BOT_R[0], ESHEL_ROAD_BOT_R[1]-2*LANE_W-(SHAKED_SIDEWK_BOT_R[1]+2*LANE_W)))
RIGHT_PL_BORDER_RECT = pygame.Rect((EREZ_ROTEM_SIDEWK_TOP_R[0], SHAKED_SIDEWK_BOT_R[1]+2*LANE_W), (CLIP_LEFT-LANE_W-(EREZ_ROTEM_SIDEWK_TOP_R[0]), ESHEL_ROAD_BOT_R[1]-(SHAKED_SIDEWK_BOT_R[1]+1.5*LANE_W)))

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

#-------------------------------------------------------------------------
# Finish Line Definitions
FINISH_LINE_RECT = pygame.Rect((EREZ_ROTEM_SIDEWK_TOP_R[0]+2*LANE_W, ROTEM_ROAD_BOT_R[1]), (40, 20))
    
FINISH_LINE_HORI = stretch_image(pygame.image.load(PATH + "Dashboard/finish_line.png"),0.5,0.7)
FINISH_LINE_VERT = pygame.transform.rotate(FINISH_LINE_HORI,90)


FINISH_LINE_IMGS = [
                    # exit right pl - enter Rotem
                    (FINISH_LINE_HORI, (EREZ_ROTEM_SIDEWK_TOP_R[0]+2*LANE_W, ROTEM_ROAD_BOT_R[1])),
                    
                    # Yaar after turn right from Rotem
                     
                    ]
#-------------------------------------------------------------------------

def draw_borders():

    def draw_road_borders():
        """
        Rect(left, top, width, height) -> Rect
        Rect((left, top), (width, height)) -> Rect
        """
        #pygame.draw.rect(WIN,RED,LEFT_PL_BORDER_RECT,5)
        #pygame.draw.rect(WIN,RED,RIGHT_PL_BORDER_RECT,5)

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
        #pygame.draw.circle(WIN,RED,RBT_LEFT_CENTER,RADIUS+1.5*LANE_W,1)
        #pygame.draw.circle(WIN,RED,RBT_RIGHT_CENTER,RADIUS+1.5*LANE_W,1)
            # Roundabouts - inner ring
        pygame.draw.circle(WIN,RED,RBT_LEFT_CENTER,RADIUS-1.3*LANE_W,1)
        pygame.draw.circle(WIN,RED,RBT_RIGHT_CENTER,RADIUS-1.3*LANE_W,1)

    def draw_lane_borders():
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
        pygame.draw.line(WIN, GREEN, (YAAR_ROAD_BOT_L[0]+1.1*LANE_W, YAAR_SIDEW_BOT_L[1]), (YAAR_ROAD_BOT_L[0]+1.1*LANE_W, ESHEL_ROAD_BOT_R[1]-LANE_W), 1)
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
        
            # Roundabouts
        pygame.draw.circle(WIN,GREEN,RBT_LEFT_CENTER,RADIUS,1)
        pygame.draw.circle(WIN,GREEN,RBT_RIGHT_CENTER,RADIUS,1)
    
    def draw_parallel_parking_borders():
        # Yaar - Horizontal
            # Top spot
        pygame.draw.line(WIN, ORANGE, (YAAR_ROAD_MID_R[0], ROTEM_ROAD_BOT_R[1]+4*LANE_W), (YAAR_ROAD_MID_R[0]+LANE_W, ROTEM_ROAD_BOT_R[1]+4*LANE_W), 1)
            # Bottom spot
        pygame.draw.line(WIN, ORANGE, (YAAR_ROAD_MID_R[0], ESHEL_ROAD_BOT_R[1]-LANE_W), (YAAR_ROAD_MID_R[0]+LANE_W, ESHEL_ROAD_BOT_R[1]-LANE_W), 1)


        # Eshel - Vertical
            # Left
        pygame.draw.line(WIN, ORANGE, (4.1*LANE_W,ESHEL_ROAD_BOT_R[1]), (4.1*LANE_W, ESHEL_ROAD_BOT_R[1]+LANE_W), 1) 
            # Right
        pygame.draw.line(WIN, ORANGE, (6.1*LANE_W,ESHEL_ROAD_BOT_R[1]), (6.1*LANE_W, ESHEL_ROAD_BOT_R[1]+LANE_W), 1) 

    draw_road_borders()
    draw_lane_borders()
    draw_parallel_parking_borders()

def draw_street_names():

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
            street_text = pygame.transform.rotate(street_text,90)
            
        street_text_pos = (pos[0]+street_text.get_rect().centerx, pos[1]+street_text.get_rect().centery)
        WIN.blit(street_text, street_text_pos)  