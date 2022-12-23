import math
import pygame

from utils import blit_rotate_center
from constants import BLUE, ELLA_ROAD_TOP_L, DASHBOARD_HOR_TOP, DASHBOARD_VERT_LEFT
class RoadUser(pygame.sprite.Sprite):

    def __init__(self, start_pos):
        # Call the parent class's constructor
        pygame.sprite.Sprite.__init__(self)

        self.image = self.IMG
        self.start_pos = start_pos
        self.rect = self.image.get_rect(topleft = start_pos)

        self.max_vel = 3
        self.acceleration = 0.02
        self.rotation_vel = 2

        self.vel = 0
        self.angle = 0
        self.x, self.y = start_pos
        

    def rotate(self, left = False, right = False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate_center(win,self.image, (self.x, self.y), self.angle)
        pygame.draw.rect(win,BLUE,self.rect,2)

    def stay_within_screen_borders(self, new_x, new_y):
        
        # Check if the new position for player car is colliding with the screen boundaries

        if new_y <= ELLA_ROAD_TOP_L[1] - self.rect.height:
            self.y = ELLA_ROAD_TOP_L[1] - self.rect.height
            self.vel = 0
        elif new_y >= DASHBOARD_HOR_TOP - self.rect.height:
            self.y = DASHBOARD_HOR_TOP - self.rect.height
            self.vel = 0
        else:
            self.y = new_y

        if new_x <= 0:
            self.x = 0
            self.vel = 0
        elif new_x >= DASHBOARD_VERT_LEFT - self.rect.height:
            self.x = DASHBOARD_VERT_LEFT - self.rect.height
            self.vel = 0
        else:
            self.x = new_x
        

    def move_forward(self):
        # Increase velocity without going over maximum velocity
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        # We want the max velocity backwards to be half of the max velocity forward
        # (Reverse gear cant reach top speed like forward gears)
        self.vel = max(self.vel - self.acceleration, -self.max_vel / 2)
        self.move()

    def move(self):
        # Using basic Trigonometry, calculate vertical and horizontal movement 
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        # Move the car in whatever direction it is facing
        new_y = self.y - vertical
        new_x = self.x - horizontal

        self.stay_within_screen_borders(new_x,new_y)

        self.rect.topleft = (self.x,self.y)

    def collide(self, mask, x = 0, y = 0):
        car_mask = pygame.mask.from_surface(self.img)

        # Calculate displacement between the 2 masks
        offset = (int(self.x - x), int(self.y - y))

        # Point of intersection - if there was poi, the objects did collide
        poi = mask.overlap(car_mask, offset) 
        return poi

    def reset(self):
        self.x, self.y = self.start_pos
        self.angle = 0
        self.vel = 0

    
