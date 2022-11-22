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