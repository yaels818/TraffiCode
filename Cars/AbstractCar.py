import math
import pygame

from utils import blit_rotate_center

class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.08 

    def rotate(self, left = False, right = False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate_center(win,self.img, (self.x, self.y), self.angle)

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
        self.y -= vertical
        self.x -= horizontal

    def collide(self, mask, x = 0, y = 0):
        car_mask = pygame.mask.from_surface(self.img)

        # Calculate displacement between the 2 masks
        offset = (int(self.x - x), int(self.y - y))

        # Point of intersection - if there was poi, the objects did collide
        poi = mask.overlap(car_mask, offset) 
        return poi

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0
