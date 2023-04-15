"""
Author: @yaels818 
Description: Pedestrian module, contains pedestrian sprites
(the player must avoid crashing into them)
"""

import pygame, math, random

from RoadUsers import RoadUser
from constants import RED_GIRL, GREEN_GIRL, OLD_MAN, BLOND_BOY, PED_PATH_ROTEM_SW_TILL_ELLA, PED_PATH_YAAR_SW_TILL_ROTEM_SW, PED_PATH_YAAR_SW_TILL_RBT, PED_PATH_ELLA_TILL_ESHEL

class Pedestrian(RoadUser):

    path = None

    def __init__(self):
        """
        Parameters
        ----------
        start_pos : (x,y)
            The first point where the sprite will appear
        current_point : int
            The number of the current point in the sprite's PATH
        vel : int
            The velocity of the sprite (default is 1)
        """
        def randomize_ped():

            dice = random.randint(1,4)
                    
            if dice == 1:
                IMG = RED_GIRL
            elif dice == 2:
                IMG = GREEN_GIRL
            elif dice == 3:
                IMG = OLD_MAN
            elif dice == 4:
                IMG = BLOND_BOY

            dice = random.randint(1,4)

            if dice == 1:
                path = PED_PATH_ROTEM_SW_TILL_ELLA
            elif dice == 2:
                path = PED_PATH_YAAR_SW_TILL_ROTEM_SW
            elif dice == 3:
                path = PED_PATH_YAAR_SW_TILL_RBT
            elif dice == 4:
                path = PED_PATH_ELLA_TILL_ESHEL

            return IMG, path
            
        IMG, self.path = randomize_ped()
        
        RoadUser.__init__(self, IMG, self.path[0])
        self.current_point = 0
        # Computer car will be moving at max velocity all the time, no acceleration
        self.vel = 1

    def reduce_speed(self):
        # Reduce the velocity by half the acceleration, if negative then just stop moving 
        self.vel = max(self.vel - self.acceleration/2, 0)
        self.move()

    def draw_points(self, win):
        for point in self.path:
            # Draw a red point of radius 5 in the path
            pygame.draw.circle(win, (255,0,0), point, 5)
        
    def calculate_angle(self):
        # Get coordinates for target point
        target_x, target_y = self.path[self.current_point]
        x_diff = target_x - self.x
        y_diff = target_y - self.y

        if y_diff == 0:
            # If there is no y difference then the car is horizontal to the point, so either 90 or 270 degrees
            desired_radian_angle = math.pi / 2
        else:
            # The angle between the car and the target point
            desired_radian_angle = math.atan(x_diff / y_diff) # arctan()

        # If the target is downwards from the car
        if target_y > self.y:
            # Correct the angle to make sure the car will be heading in the correct direction
            desired_radian_angle += math.pi

        difference_in_angle = self.angle - math.degrees(desired_radian_angle)

        # If the difference is drastic, then there is a more efficient angle to get to the target point
        if difference_in_angle >= 180:
            difference_in_angle -= 360

        # Make sure the car doesnt over/undershoot the angle (avoid stuttering and over-corrections)
        if difference_in_angle > 0:
            # If the diff is less than rotation_vel we will snap immediately to the diff angle and stay on it
            self.angle -= min(self.rotation_vel, abs(difference_in_angle))
        else:
            self.angle += min(self.rotation_vel, abs(difference_in_angle))    

    def update_path_point(self):
            # Get the next target point from the pre-made path
            target = self.path[self.current_point]

            # Create a rectangle with the car as top-left corner 
            # (because we have the img but the img doesn't know where it is)
            rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

            # If we collided with a target point, move on to the next one
            if rect.collidepoint(*target):
                self.current_point += 1

    def move(self):
        # If there is no point to move to
        if self.current_point >= len(self.path):
            self.kill()
            return

        # Calculate and shift the car to the needed angle for the next point
        self.calculate_angle()

        # See if we need to move to the next point
        self.update_path_point()
        super().move()
    
    def next_level(self, level):
    
        # Increase computer's vel 0.2 each level - will never go faster than the player's
        self.vel = self.max_vel + (level + 1) * 0.2

        self.current_point = 0