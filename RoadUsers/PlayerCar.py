"""
Author: @yaels818
Description: PlayerCar module, contains the player's car sprite
            (inherits from RoadUser).
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
                self.angle -= 360   
            
        elif right:
            self.angle -= self.rotation_vel
            # Bind angle to stay within 0 and 360
            if self.angle <= 0:
                self.angle += 360

    def move_forward(self):
        # Increase velocity without going over maximum velocity
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        # We want the max velocity backwards to be half of the max velocity forward
        # (Reverse gear cant reach top speed like forward gears)
        self.vel = max(self.vel - self.acceleration, -self.max_vel / 2)
        self.move()
                    
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

    def check_collision_with_mask(self, mask, scene_offset_x, scene_offset_y):
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
        displacement = (int(self.x - scene_offset_x), int(self.y - scene_offset_y))

        # Find poi (= Point of Intersection) 
        # -> if there is a poi, the objects are colliding
        poi = mask.overlap(car_mask, displacement)
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
