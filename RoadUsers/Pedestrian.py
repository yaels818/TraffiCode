"""
Author: @yaels818 
Description: Pedestrian module, contains pedestrian sprites
(the player must avoid crashing into them)
"""

import random

from RoadUsers import RoadUser
from constants import RED_GIRL, GREEN_GIRL, OLD_MAN, BLOND_BOY, \
        PED_PATH_ROTEM_SW_TILL_ELLA, PED_PATH_YAAR_SW_TILL_ROTEM_SW, \
        PED_PATH_YAAR_SW_TILL_RBT, PED_PATH_ELLA_TILL_ESHEL

class Pedestrian(RoadUser):

    path = None

    def __init__(self):
        """
        Initialize the pedestrian.

        Parameters
        ----------
        self : Pedestrian
            The pedestrian object
        """

        def randomize_ped():
            """
            Choose the ped's image and path by random. 
            """
            # Pick a random number to decide the ped's image
            dice = random.randint(1,4)
                    
            if dice == 1:
                IMG = RED_GIRL
            elif dice == 2:
                IMG = GREEN_GIRL
            elif dice == 3:
                IMG = OLD_MAN
            elif dice == 4:
                IMG = BLOND_BOY

            # Pick a random number to decide the ped's path
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

        # Pick ped's image and path by random    
        IMG, self.path = randomize_ped()
        
        # Initialize the pedestrian
        RoadUser.__init__(self, IMG, self.path[0])

        # Ped's current point in its path
        self.current_point = 0

        # Ped's initial velocity
        self.vel = 1
    
    def next_level(self, level):
    
        # Increase the ped's vel 0.2 each level
        self.vel = self.max_vel + (level + 1) * 0.2

        self.current_point = 0