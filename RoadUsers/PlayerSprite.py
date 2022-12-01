import pygame

from RoadUsers import RoadUser
import constants

class PlayerSprite(RoadUser, pygame.sprite.Sprite):

    IMG = constants.RED_CAR
    START_POS = (150,150)

    def __init__(self,max_vel, rotation_vel):
        # Call the parent class's constructor
        pygame.sprite.Sprite.__init__(self)
        RoadUser.__init__(self,max_vel, rotation_vel)
        self.image = constants.RED_CAR
        self.rect = self.image.get_rect(center = self.START_POS)

    def reduce_speed(self):
        # Reduce the velocity by half the acceleration, if negative then just stop moving 
        self.vel = max(self.vel - 2 * self.acceleration, 0)
        self.move()

    def bounce(self):
        # Bounce back from a wall
        self.vel = -self.vel/2
        self.move()

    def reset(self):
         RoadUser().reset()

