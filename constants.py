# Outsource Imports
import pygame
import os

# Local Imports
from utils import scale_image

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
SMALL_FONT = pygame.font.SysFont("erasdemiitc", 26)
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
PHONE_CENTER = WIDTH - WIDTH/9
PHONE_LEFT = WIDTH - WIDTH/4.7
LIGHTS_BTN_CENTER = WIDTH-PHONE_CENTER
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
PHONE = scale_image(pygame.image.load(PATH + "Dashboard/phone.png"),0.55)

FINISH_LINE_VERT = scale_image(pygame.image.load(PATH + "Dashboard/finish_line.png"),0.68)
FINISH_LINE_HORI = pygame.transform.rotate(FINISH_LINE_VERT,90)

# Position Definitions - center
SPEEDOMETER_POS = (MIRROR_CENTER-SPEEDOMETER.get_rect().centerx, DASHBOARD_HOR_TOP-SPEEDOMETER.get_rect().centery/2)
MIRROR_POS = (MIRROR_CENTER-MIRROR.get_rect().centerx, MIRROR.get_rect().centery/3)
PHONE_POS = (PHONE_CENTER-PHONE.get_rect().centerx,HEIGHT-DASHBOARD_HOR_TOP-PHONE.get_rect().centery/4)
DASH_IMGS = [(SPEEDOMETER, SPEEDOMETER_POS), (MIRROR, MIRROR_POS),(PHONE, PHONE_POS)]

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
MUSIC_BTN_POS = (PHONE_CENTER-BTN_IMGS_OFF[5].get_rect().centerx/2, DASHBOARD_HOR_TOP)

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
RED_CAR = scale_image(pygame.image.load(PATH + "Cars/red_car.png"), 0.3)
#-------------------------------------------------------------------------
# Road Definitions
LANE_W = 22 # Lane Width in px

YAAR_ROAD_BOT_L = (LEFT_BLINK_POS[0] + BTN_IMGS_OFF[1].get_rect().centerx/2, HEIGHT-HEIGHT/3+5)
YAAR_ROAD_MID_R = (YAAR_ROAD_BOT_L[0] + 4.2*LANE_W, HEIGHT-HEIGHT/3+5)
EREZ_ROAD_BOT_L = (MIRROR_CENTER/3+LANE_W, HEIGHT/6.2)
ELLA_ROAD_TOP_L = (MIRROR_CENTER/3,HEIGHT/6.2)
ESHEL_ROAD_BOT_R = (YAAR_ROAD_MID_R[0]+LANE_W,HEIGHT-HEIGHT/4+2)
ROTEM_ROAD_BOT_R = (MIRROR_CENTER*1.5-0.5*LANE_W,HEIGHT/2 - 2.2*LANE_W + 2*LANE_W)

    # Sidewalks    
SHAKED_SIDEWK_BOT_R = (MIRROR_CENTER/2-4*LANE_W, HEIGHT/2 - 2.2*LANE_W)
EREZ_ROTEM_SIDEWK_TOP_R = (YAAR_ROAD_MID_R[0]+6*LANE_W, HEIGHT/6.2 + 2*LANE_W)

    # Roundabouts
LEFT_ROUNDABOUT_CENTER = (MIRROR_CENTER/2+LANE_W, SHAKED_SIDEWK_BOT_R[1]+LANE_W)
RIGHT_ROUNDABOUT_CENTER = (MIRROR_CENTER*1.5-2*LANE_W, EREZ_ROTEM_SIDEWK_TOP_R[1]+LANE_W)

FINISH_LINE_IMGS = [(FINISH_LINE_HORI, (EREZ_ROTEM_SIDEWK_TOP_R[0]+1.5*LANE_W,LEFT_ROUNDABOUT_CENTER[1]))]

def draw_borders():

    # Road Borders
        # HaErez - Top Road 
        # Horizontal
            # Top (border with sky)
    pygame.draw.line(WIN, RED, (MIRROR_CENTER/3, ELLA_ROAD_TOP_L[1]), (EREZ_ROTEM_SIDEWK_TOP_R[0]+2*LANE_W, ELLA_ROAD_TOP_L[1]), 1)
            # Top (border with park)
    pygame.draw.line(WIN, RED, (EREZ_ROTEM_SIDEWK_TOP_R[0]+2*LANE_W, EREZ_ROTEM_SIDEWK_TOP_R[1]), (RIGHT_ROUNDABOUT_CENTER[0]-3.25*LANE_W, EREZ_ROTEM_SIDEWK_TOP_R[1]), 1)
            # Bottom - Ella till Hadas
    pygame.draw.line(WIN, RED, (MIRROR_CENTER/3+LANE_W, EREZ_ROTEM_SIDEWK_TOP_R[1]), (MIRROR_CENTER/2, EREZ_ROTEM_SIDEWK_TOP_R[1]), 1)
            # Bottom - Hadas till Yaar
    pygame.draw.line(WIN, RED, (MIRROR_CENTER/2+2*LANE_W+2, EREZ_ROTEM_SIDEWK_TOP_R[1]), (YAAR_ROAD_BOT_L[0], EREZ_ROTEM_SIDEWK_TOP_R[1]), 1)
            # Bottom - Yaar till Erez 
    pygame.draw.line(WIN, RED, (YAAR_ROAD_MID_R[0], EREZ_ROTEM_SIDEWK_TOP_R[1]), (EREZ_ROTEM_SIDEWK_TOP_R[0], EREZ_ROTEM_SIDEWK_TOP_R[1]), 1)
            # Bottom - Erez till Rotem
    pygame.draw.line(WIN, RED, (EREZ_ROTEM_SIDEWK_TOP_R[0], EREZ_ROTEM_SIDEWK_TOP_R[1]+2*LANE_W), (RIGHT_ROUNDABOUT_CENTER[0]-3.25*LANE_W, EREZ_ROTEM_SIDEWK_TOP_R[1]+2*LANE_W), 1)
        # Vertical
            # Top - Erez till Rotem
    pygame.draw.line(WIN, RED, (EREZ_ROTEM_SIDEWK_TOP_R[0]+2*LANE_W, ELLA_ROAD_TOP_L[1]), (EREZ_ROTEM_SIDEWK_TOP_R[0]+2*LANE_W,EREZ_ROTEM_SIDEWK_TOP_R[1]), 1)
            # Bottom - Erez till Rotem
    pygame.draw.line(WIN, RED, (EREZ_ROTEM_SIDEWK_TOP_R[0], EREZ_ROTEM_SIDEWK_TOP_R[1]), (EREZ_ROTEM_SIDEWK_TOP_R[0],EREZ_ROTEM_SIDEWK_TOP_R[1]+2*LANE_W), 1)

        # HaElla - One Way Road
        # Vertical
    pygame.draw.line(WIN, RED, (SHAKED_SIDEWK_BOT_R[0],HEIGHT/6.2), (SHAKED_SIDEWK_BOT_R[0],ESHEL_ROAD_BOT_R[1]-2*LANE_W), 1)

        # HaYaar - Main Road
            # Vertical - Left
    pygame.draw.line(WIN, RED, (YAAR_ROAD_BOT_L[0], EREZ_ROTEM_SIDEWK_TOP_R[1]), (YAAR_ROAD_BOT_L[0], YAAR_ROAD_BOT_L[1]), 1)
            # Verical - Right
    pygame.draw.line(WIN, RED, (YAAR_ROAD_MID_R[0], EREZ_ROTEM_SIDEWK_TOP_R[1]), (YAAR_ROAD_MID_R[0], SHAKED_SIDEWK_BOT_R[1]+4*LANE_W), 1)
            # Horizontal
    pygame.draw.line(WIN, RED, (0, SHAKED_SIDEWK_BOT_R[1]), (SHAKED_SIDEWK_BOT_R[0], SHAKED_SIDEWK_BOT_R[1]), 1)
    
        # HaHadas - Vertical
            # Left - Erez till Hadas
    pygame.draw.line(WIN, RED, (MIRROR_CENTER/2,EREZ_ROTEM_SIDEWK_TOP_R[1]), (MIRROR_CENTER/2, SHAKED_SIDEWK_BOT_R[1]-2.25*LANE_W), 1)
            # Left - Hadas till Eshel
    pygame.draw.line(WIN, RED, (MIRROR_CENTER/2,LEFT_ROUNDABOUT_CENTER[1]+3.25*LANE_W), (MIRROR_CENTER/2, ESHEL_ROAD_BOT_R[1]-2*LANE_W), 1)
    
        # HaRotem - Horizontal
    pygame.draw.line(WIN, RED, (YAAR_ROAD_MID_R[0], SHAKED_SIDEWK_BOT_R[1]), (RIGHT_ROUNDABOUT_CENTER[0]-1.5*LANE_W, SHAKED_SIDEWK_BOT_R[1]), 1)
    pygame.draw.line(WIN, RED, (YAAR_ROAD_MID_R[0], ROTEM_ROAD_BOT_R[1]), (ROTEM_ROAD_BOT_R[0], ROTEM_ROAD_BOT_R[1]), 1)

        # HaEshel - Horizontal
            # Bottom
    pygame.draw.line(WIN, RED, (0,ESHEL_ROAD_BOT_R[1]), (ESHEL_ROAD_BOT_R[0], ESHEL_ROAD_BOT_R[1]), 1) 


        # Roundabouts - outer ring
    pygame.draw.circle(WIN,RED,LEFT_ROUNDABOUT_CENTER,RADIUS+1.5*LANE_W,1)
    pygame.draw.circle(WIN,RED,RIGHT_ROUNDABOUT_CENTER,RADIUS+1.5*LANE_W,1)

        # Roundabouts - inner ring
    pygame.draw.circle(WIN,RED,LEFT_ROUNDABOUT_CENTER,RADIUS-1.3*LANE_W,1)
    pygame.draw.circle(WIN,RED,RIGHT_ROUNDABOUT_CENTER,RADIUS-1.3*LANE_W,1)

    # Lane Borders
        # Top Road - Horizontal
    pygame.draw.line(WIN, GREEN, (MIRROR_CENTER/3+LANE_W, HEIGHT/5.1), (EREZ_ROTEM_SIDEWK_TOP_R[0]+LANE_W, HEIGHT/5.1), 1) # Top Road
        # Bottom - main sidewalk till right roundabout
    pygame.draw.line(WIN, GREEN, (EREZ_ROTEM_SIDEWK_TOP_R[0]+LANE_W, EREZ_ROTEM_SIDEWK_TOP_R[1]+LANE_W), (RIGHT_ROUNDABOUT_CENTER[0], EREZ_ROTEM_SIDEWK_TOP_R[1]+LANE_W), 1)

        # Main Road - Vertical - Left Lane Line
    pygame.draw.line(WIN, GREEN, (YAAR_ROAD_BOT_L[0]+1.1*LANE_W, HEIGHT/5.1), (YAAR_ROAD_BOT_L[0]+1.1*LANE_W, HEIGHT-HEIGHT/4+2), 1)
        # Main Road - Vertical - Continuous Lane Line
    pygame.draw.line(WIN, GREEN, (YAAR_ROAD_BOT_L[0]+2.2*LANE_W, HEIGHT/5.1), (YAAR_ROAD_BOT_L[0]+2.2*LANE_W, HEIGHT-HEIGHT/4+2), 1)
        # Main Road - Vertical - Right Lane Line
    pygame.draw.line(WIN, GREEN, (YAAR_ROAD_MID_R[0]-LANE_W, HEIGHT/5.1), (YAAR_ROAD_MID_R[0]-LANE_W, HEIGHT-HEIGHT/4+2), 1)
    
    
        # Roundabouts
    pygame.draw.circle(WIN,GREEN,LEFT_ROUNDABOUT_CENTER,RADIUS,1)
    pygame.draw.circle(WIN,GREEN,RIGHT_ROUNDABOUT_CENTER,RADIUS,1)
    
    # Crosswalks

    # Parking lots
        # Left PL
        # Horizontal - Right Entry
    #pygame.draw.line(WIN, BLUE, (0,HEIGHT/2), (MIRROR_CENTER/3, HEIGHT/2), 1)   # Top
            # Vertical - Top Entry
    pygame.draw.line(WIN, BLUE, (WIDTH-PHONE_CENTER-LANE_W,HEIGHT/2-5), (WIDTH-PHONE_CENTER-LANE_W, HEIGHT-HEIGHT/3+5), 1) # Left
    pygame.draw.line(WIN, BLUE, (WIDTH-PHONE_CENTER,HEIGHT/2-5), (WIDTH-PHONE_CENTER, HEIGHT-HEIGHT/3+5), 1)    # Right

            # Horizontal - Right Entry
            
    pygame.draw.line(WIN, BLUE, (0,HEIGHT/2+HEIGHT/10), (MIRROR_CENTER/3, HEIGHT/2+HEIGHT/10), 1)    # Bottom

            # Horizontal - Above Bottom
    pygame.draw.line(WIN, BLUE, (0,HEIGHT/2+HEIGHT/7.8), (MIRROR_CENTER/3, HEIGHT/2+HEIGHT/7.8), 1)

def draw_street_names():

    STREETS = [ ("HaErez", (LEFT_ROUNDABOUT_CENTER[0]-2*LANE_W,EREZ_ROTEM_SIDEWK_TOP_R[1]-2*LANE_W)),
                ("HaErez", (YAAR_ROAD_MID_R[0],EREZ_ROTEM_SIDEWK_TOP_R[1]-LANE_W)),
                ("HaHadas", (LEFT_ROUNDABOUT_CENTER[0]-2.2*LANE_W,EREZ_ROTEM_SIDEWK_TOP_R[1]+3*LANE_W)), 
                ("HaRotem", (RIGHT_ROUNDABOUT_CENTER[0]-2.5*LANE_W,EREZ_ROTEM_SIDEWK_TOP_R[1]+3*LANE_W)),
                ("HaRotem", (EREZ_ROTEM_SIDEWK_TOP_R[0]+1.5*LANE_W,LEFT_ROUNDABOUT_CENTER[1])),
                ("HaYaar", (YAAR_ROAD_MID_R[0]-4*LANE_W,LEFT_ROUNDABOUT_CENTER[1]-LANE_W)),
                ("HaElla", (SHAKED_SIDEWK_BOT_R[0],SHAKED_SIDEWK_BOT_R[1]-2.5*LANE_W)),
                ("HaElla", (SHAKED_SIDEWK_BOT_R[0],SHAKED_SIDEWK_BOT_R[1]+LANE_W)),
                ("HaShaked",(0,LEFT_ROUNDABOUT_CENTER[1])),
                ("HaEshel", (SHAKED_SIDEWK_BOT_R[0]-2*LANE_W,DASHBOARD_HOR_TOP-4*LANE_W))]
    
    for streetName, pos in STREETS:
        street_text = STREETS_FONT.render(streetName,1,PINK)
        if streetName == "HaElla":
            street_text = pygame.transform.rotate(street_text,90)
            
        street_text_pos = (pos[0]+street_text.get_rect().centerx, pos[1]+street_text.get_rect().centery)
        WIN.blit(street_text, street_text_pos)  


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

    
    pygame.draw.line(WIN, PINK, (MIRROR_CENTER - (MIRROR_CENTER/2 - MIRROR_CENTER/4),0), (MIRROR_CENTER - (MIRROR_CENTER/2 - MIRROR_CENTER/4), HEIGHT), 1)    # Left Roundabout left line

    # Horizontal
    pygame.draw.line(WIN, RED, (0, HEIGHT/2), (WIDTH, HEIGHT/2), 1)
    pygame.draw.line(WIN, BLUE, (0, HEIGHT/3), (WIDTH, HEIGHT/3), 1)
    pygame.draw.line(WIN, GREEN, (0, HEIGHT/2 + HEIGHT/4), (WIDTH, HEIGHT/2 + HEIGHT/4), 1)
    pygame.draw.line(WIN, RED, (0, HEIGHT/2 - HEIGHT/4), (WIDTH, HEIGHT/2 - HEIGHT/4), 1)
    
