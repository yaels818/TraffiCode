import pygame

from RoadUsers import RoadUser
from constants import RED_CAR

class PlayerSprite(RoadUser):

    IMG = RED_CAR

    def __init__(self,start_pos):
        RoadUser.__init__(self,start_pos)

    def original_reduce_speed(self):
        # Reduce the velocity by half the acceleration, if negative then just stop moving 
        self.vel = max(self.vel - self.acceleration/2, 0)
        self.move()

    def reduce_speed(self, emergency_brake = False):
        if emergency_brake:
            # Reduce the velocity by twice the acceleration, if negative then just stop moving 
            self.vel = max(self.vel - 2*self.acceleration, 0)
        else:
            # Reduce the velocity by half the acceleration, if negative then just stop moving 
            self.vel = max(self.vel - self.acceleration/2, 0)
            self.move()

    def bounce(self):
        # Bounce back from a wall
        self.vel = -self.vel/2
        self.move()

    def reset(self):
         RoadUser().reset()
