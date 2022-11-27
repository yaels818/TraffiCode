import pygame

from utils import scale_image
import constants
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

def create_buttons_list():

    menu_btn = DashboardButton(*constants.MENU_BTN_BLP)
    lights_btn = DashboardButton(*constants.LIGHTS_BTN_BLP)
    left_blinker_btn = DashboardButton(*constants.LEFT_BLINK_BLP)
    right_blinker_btn = DashboardButton(*constants.RIGHT_BLINK_BLP)
    wipers_btn = DashboardButton(*constants.WIPERS_BTN_BLP)
    ac_btn = DashboardButton(*constants.AC_BTN_BLP)
    music_btn = DashboardButton(*constants.MUSIC_BTN_BLP)

    buttons_list = [lights_btn,left_blinker_btn,right_blinker_btn,wipers_btn,ac_btn,music_btn,menu_btn]
    return buttons_list