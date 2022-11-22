import pygame

from RoadUsers import AbstractCar
import constants

class PlayerSprite(AbstractCar, pygame.sprite.Sprite):

    IMG = constants.RED_CAR
    START_POS = (150,150)

    def __init__(self):
        # Call the parent class's constructor
        pygame.sprite.Sprite.__init__(self)
        AbstractCar.__init__(self,2,2)
        self.image = constants.RED_CAR
        self.rect = self.image.get_rect(center = self.START_POS)

    def reduce_speed(self):
        # Reduce the velocity by half the acceleration, if negative then just stop moving 
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self):
        # Bounce back from a wall
        self.vel = -self.vel/2
        self.move()

    def reset(self):
         AbstractCar().reset()

