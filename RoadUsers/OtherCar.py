"""
Author: @yaels818
Description: OtherCar module, contains other car sprites 
(the player must avoid crashing into them)
"""

import random

from RoadUsers import RoadUser
from constants import YELLOW_CAR, WHITE_TRUCK, BLUE_VAN ,\
    CAR_PATH_YAAR_TILL_LEFT_PL, CAR_PATH_ESHEL_TILL_ROTEM, \
    CAR_PATH_ELLA_TILL_RIGHT_PL, CAR_PATH_ROTEM_TILL_SHAKED

class OtherCar(RoadUser):

    #path_exp = []

    def __init__(self, vel):

        def randomize_car():
     
            dice = random.randint(1,3)
                    
            if dice == 1:
                IMG = YELLOW_CAR
            elif dice == 2:
                IMG = WHITE_TRUCK
            elif dice == 3:
                IMG = BLUE_VAN

            
            dice = random.randint(1,4)

            if dice == 1:
                path = CAR_PATH_YAAR_TILL_LEFT_PL
            elif dice == 2:
                path = CAR_PATH_ESHEL_TILL_ROTEM
            elif dice == 3:
                path = CAR_PATH_ELLA_TILL_RIGHT_PL
            elif dice == 4:
                path = CAR_PATH_ROTEM_TILL_SHAKED
            
            return IMG, path

        IMG, self.path = randomize_car()
        
        RoadUser.__init__(self, IMG, self.path[0])

        self.current_point = 0
        self.vel = vel
        