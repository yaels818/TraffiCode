import pygame
from utils import scale_image

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

def load_button_images():
    
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

    buttons_list = [lights_btn,left_blinker_btn,right_blinker_btn,wipers_btn,ac_btn,music_btn,menu_btn]
    return buttons_list