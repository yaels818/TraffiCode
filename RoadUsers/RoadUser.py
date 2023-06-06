"""
Author: @yaels818
Description: RoadUser module, contains RoadUser sprites
(inherited by PlayerCar, OtherCar and Pedestrian)
"""

import pygame, math

from constants import WIN, BLUE, ELLA_ROAD_TOP_L, DASHBOARD_HOR_TOP, DASHBOARD_VERT_LEFT
from utils import blit_rotate_center

class RoadUser(pygame.sprite.Sprite):

    def __init__(self, IMG, START_POS):
        # Call the parent class's constructor
        pygame.sprite.Sprite.__init__(self)

        self.image = IMG
        self.start_pos = START_POS
        self.rect = self.image.get_rect(topleft = START_POS)

        self.max_vel = 2
        self.acceleration = 0.01
        self.rotation_vel = 1.5

        self.vel = 0
        self.angle = 0
        self.x, self.y = START_POS
        
    def draw(self):
        """
        Draw the sprite image of the car in its current position and current angle.
        Update the bounding rectangle of the car accordingly.
        """
        self.rect = blit_rotate_center(WIN, self.image, (self.x, self.y), self.angle)
        
        # Shrink sprite's hit box (to give players a bit more room before collisions)
        self.rect = self.rect.inflate(-5,-3)
        
        #pygame.draw.rect(WIN, BLUE, self.rect, 1)
    
    def stay_within_scene_borders(self, new_x, new_y):
        """
        Check if the new position for player car is colliding with the screen boundaries
        """

        # Check collision with top edge of the scene
        if new_y <= ELLA_ROAD_TOP_L[1] - self.rect.height:
            self.y = ELLA_ROAD_TOP_L[1] - self.rect.height
            self.vel = 0
        # Check collision with bottom edge of the scene
        elif new_y >= DASHBOARD_HOR_TOP - self.rect.height:
            self.y = DASHBOARD_HOR_TOP - self.rect.height
            self.vel = 0
        else:
            self.y = new_y

        # Check collision with left edge of the scene
        if new_x <= 0 - self.rect.height/2:  
            self.x = 0 - self.rect.height/2
            self.vel = 0
        # Check collision with right edge of the scene
        elif new_x >= DASHBOARD_VERT_LEFT - self.rect.height/2:
            self.x = DASHBOARD_VERT_LEFT - self.rect.height/2
            self.vel = 0
        else:
            self.x = new_x

    def move(self):
        # Using basic Trigonometry, calculate vertical and horizontal movement 
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        # Calculate the new position for the car in the direction it is facing
        new_y = self.y - vertical
        new_x = self.x - horizontal

        # Make sure the new position can't be beyond scene borders
        self.stay_within_scene_borders(new_x, new_y)

        # Update the car bounding rect
        self.rect.topleft = (self.x, self.y) 
    
    def move_sprite(self):
        # If there is no point to move to
        if self.current_point >= len(self.path):
            self.kill()
            return

        # Calculate and shift the sprite to the needed angle 
        # for the current target point
        self.calculate_angle()

        # Get the next target point and move towards it
        self.update_path_point()
        self.move()

    def reduce_sprite_speed(self):
        """
        Reduce sprite's velocity.
        """
        # Reduce the velocity by half the acceleration, 
        # if negative then just stop moving 
        self.vel = max(self.vel - self.acceleration/2, 0)
        self.move()

    def calculate_angle(self):
        """
        Find the angle between current point and the next point in the path. 
        """
        # Get coordinates for target point
        target_x, target_y = self.path[self.current_point]

        # Calculate displacement between the sprite and the target point
        x_diff = target_x - self.x
        y_diff = target_y - self.y

        if y_diff == 0:
            # If there is no y difference 
            # => the car is horizontal to the point 
            # (so either 90 or 270 degrees)
            desired_radian_angle = math.pi / 2
        else:
            # The angle between the car and the target point
            # (will always return an acute angle = less than 90 degrees)
            desired_radian_angle = math.atan(x_diff / y_diff) # arctan()

        # If the target is downwards from the sprite
        # => the needed turn to get to the target point 
        # has to be more extreme than the calculated acute angle
        if target_y > self.y:
            # Correct the angle to make sure the car will be 
            # heading in the correct direction
            desired_radian_angle += math.pi

        # Convert desired_angle from radians to degrees, 
        # then calculate the difference between the sprite's current angle
        # and the desired angle 
        difference_in_angle = self.angle - math.degrees(desired_radian_angle)

        # If the difference is drastic 
        # => there is a more efficient angle to get to the target point
        if difference_in_angle >= 180:
            difference_in_angle -= 360

        # Make sure the car doesn't over/undershoot the angle 
        # (avoid stuttering and over-corrections)
        if difference_in_angle > 0:
            # If the diff is more than rotation_vel 
            # => sprite will snap immediately to the diff angle and stay on it
            self.angle -= max(self.rotation_vel, difference_in_angle)   # Right
        else:
            self.angle += max(self.rotation_vel, abs(difference_in_angle))   # Left

    def draw_points(self, color):
        """
        Draw all the points in the sprite's path. 

        Parameters
        ----------
        self : RoadUser
            The RoadUser object
        
        color : tuple
            The color for the points
        """
        for point in self.path:
            # Draw a circle in the position of this point in the path
            pygame.draw.circle(WIN, color, point, 5)
 
    def update_path_point(self):
            # Get the next target point from the pre-made path
            target = self.path[self.current_point]

            # Create a rectangle with the car as top-left corner 
            # (because we have the img but the img doesn't know where it is)
            rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

            # If we collided with a target point, move on to the next one
            if rect.collidepoint(*target):
                self.current_point += 1

    