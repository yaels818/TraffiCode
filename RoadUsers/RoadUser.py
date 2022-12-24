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

        self.max_vel = 2
        self.acceleration = 0.01
        self.rotation_vel = 2

        self.vel = 0
        self.angle = 0
        self.x, self.y = start_pos
        
    def draw(self, win):
        """
        Draw the sprite image of the car in its current position and current angle.
        Update the bounding rectangle of the car accordingly.
        """
        self.rect = blit_rotate_center(win,self.image, (self.x, self.y), self.angle)
        pygame.draw.rect(win,BLUE,self.rect,1)

    def rotate(self, left = False, right = False):
        """
        Rotate the car between 0 and 360 degrees. 
        0/360 ==> car is facing up  ^
        90 ==> car is facing left   <
        180 ==> car is facing down  V
        270 ==> car is facing right >
        """
        if left:
            self.angle += self.rotation_vel
            # Bind angle to stay within 0 and 360
            if self.angle >= 360:
                self.angle = self.angle - 360   
            
        elif right:
            self.angle -= self.rotation_vel
            # Bind angle to stay within 0 and 360
            if self.angle <= 0:
                self.angle = self.angle + 360
    
    def stay_within_scene_borders(self, new_x, new_y):
        """
        Check if the new position for player car is colliding with the screen boundaries
        """

        # Check collision with top border of the scene
        if new_y <= ELLA_ROAD_TOP_L[1] - self.rect.height:
            self.y = ELLA_ROAD_TOP_L[1] - self.rect.height
            self.vel = 0
        # Check collision with bottom border of the scene
        elif new_y >= DASHBOARD_HOR_TOP - self.rect.height:
            self.y = DASHBOARD_HOR_TOP - self.rect.height
            self.vel = 0
        else:
            self.y = new_y

        # Check collision with left border of the scene
        if new_x <= 0 + self.rect.height/2:  
            self.x = 0 + self.rect.height/2
            self.vel = 0
        # Check collision with right border of the scene
        elif new_x >= DASHBOARD_VERT_LEFT - self.rect.height/2:
            self.x = DASHBOARD_VERT_LEFT - self.rect.height/2
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

        # Calculate the new position for the car in the direction it is facing
        new_y = self.y - vertical
        new_x = self.x - horizontal

        # Make sure the new position can't be beyond scene borders
        self.stay_within_scene_borders(new_x,new_y)

        # Update the car bounding rect
        self.rect.topleft = (self.x,self.y)

    def reset(self):
        self.x, self.y = self.start_pos
        self.angle = 0
        self.vel = 0

    
