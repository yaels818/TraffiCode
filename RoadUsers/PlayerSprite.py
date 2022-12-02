import pygame

from RoadUsers import RoadUser
import constants

class PlayerSprite(RoadUser):

    IMG = constants.RED_CAR

    def __init__(self,start_pos):
        RoadUser.__init__(self,start_pos)

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

    def draw(self, win):
        RoadUser.draw(self,win)
        pygame.draw.rect(win,constants.BLUE,self.rect,2)


