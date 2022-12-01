import RoadUsers
import constants

class PlayerCar(RoadUsers.AbstractCar): # Inherit from AbstractCar
    IMG = constants.RED_CAR
    START_POS = (400, 450)

    def __init__(self,max_vel, rotation_vel) -> None:
        super().__init__(max_vel, rotation_vel)

    def reduce_speed(self):
        # Reduce the velocity by half the acceleration, if negative then just stop moving 
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self):
        # Bounce back from a wall
        self.vel = -self.vel/2
        self.move()

    def reset(self):
        super().reset()