import pygame

from RoadUsers import RoadUser
from constants import RED_CAR, PLAYER_START_POS, SCENE_HEIGHT_START

class PlayerCar(RoadUser):

    def __init__(self):
        RoadUser.__init__(self, RED_CAR, PLAYER_START_POS)

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
        self.vel = -self.vel/3
        #self.vel = 0
        self.move()

    def check_collision_with_mask(self, mask, x = 0, y = SCENE_HEIGHT_START):
        car_mask = pygame.mask.from_surface(self.image)

        # Calculate displacement between the 2 masks
        offset = (int(self.x - x), int(self.y - y))

        # Point of intersection - if there was poi, the objects did collide
        poi = mask.overlap(car_mask, offset) 
        return poi

    def reset(self):
        self.x, self.y = PLAYER_START_POS
        self.angle = 0
        self.vel = 0
