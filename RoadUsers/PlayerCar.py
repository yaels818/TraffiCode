"""
Author: @yaels818
Description: PlayerCar module, contains the player's car sprite 
"""

import pygame

from RoadUsers import RoadUser
from constants import RED_CAR, PLAYER_START_POS, SCENE_HEIGHT_START

class PlayerCar(RoadUser):

    def __init__(self):
        """
        Initialize the player's car.

        Parameters
        ----------
        self : PlayerCar
            The player's car object
        """
        RoadUser.__init__(self, RED_CAR, PLAYER_START_POS)

    def reduce_speed(self, emergency_brake = False):
        """
        Reduce player's car velocity (brake).

        Parameters
        ----------
        self : PlayerCar
            The player's car object
        emergency_brake : bool
            False = regular brake (default)
            True = emergency brake (hard brake)
        """
        if emergency_brake:
            # Reduce the velocity by twice the acceleration, 
            # if negative then just stop moving 
            self.vel = max(self.vel - 2*self.acceleration, 0)
        else:
            # Reduce the velocity by half the acceleration, 
            # if negative then just stop moving 
            self.vel = max(self.vel - self.acceleration/2, 0)
            self.move()

    def check_collision_with_mask(self, mask, x = 0, y = SCENE_HEIGHT_START):
        """
        Check if player's car is colliding with mask.

        Parameters
        ----------
        self : PlayerCar
            The player's car object
        mask : Mask
            The mask we are checking collision with
        x : int
            scene offset (x axis)
        y : int
            scene offset (y axis)
        """
        # Create mask from the car's image
        car_mask = pygame.mask.from_surface(self.image)

        # Calculate displacement between the 2 masks
        offset = (int(self.x - x), int(self.y - y))

        # Find poi (= Point of Intersection) 
        # -> if there is a poi, the objects are colliding
        poi = mask.overlap(car_mask, offset)
        return poi

    def reset(self):
        """
        Reset the player's car back to its original state at the beginning of the game.

        Parameters
        ----------
        self : PlayerCar
            The player's car object
        """
        self.x, self.y = PLAYER_START_POS
        self.angle = 0
        self.vel = 0
