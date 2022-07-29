import pygame
import time
import math
from utils import scale_image, blit_rotate_center, blit_text_center

# Load up a basic window
WIDTH, HEIGHT = 960, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TraffiCode")

pygame.font.init()
MAIN_FONT = pygame.font.SysFont("centurygothic", 36)
SMALL_FONT = pygame.font.SysFont("centurygothic", 26)

SCENE = scale_image(pygame.image.load("Assets\Images\Scenes\Mishmar HaGvul.png"),1.7)
SCENE_BORDER = scale_image(pygame.image.load("Assets\Images\Borders\Mishmar HaGvul_Border_Monocrome.png"),1.7)
RED_CAR = scale_image(pygame.image.load("Assets\Images\Cars/Audi.png"), 0.5)

# Create a mask from track border
SCENE_MASK = pygame.mask.from_surface(SCENE_BORDER)

FPS = 60    # Frame per second
clock = pygame.time.Clock()



class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.08 

    def rotate(self, left = False, right = False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate_center(win,self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        # Increase velocity without going over maximum velocity
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        # We want the max velocity backwards to be half of the max velocity forward
        # (Reverse gear cant reach top speed like forward gears)
        self.vel = max(self.vel - self.acceleration, -self.max_vel / 2)
        self.move()

    def move(self):
        # Using basic Trigonometry, calculate vertical and horizontal movement 
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        # Move the car in whatever direction it is facing
        self.y -= vertical
        self.x -= horizontal

    def collide(self, mask, x = 0, y = 0):
        car_mask = pygame.mask.from_surface(self.img)

        # Calculate displacement between the 2 masks
        offset = (int(self.x - x), int(self.y - y))

        # Point of intersection - if there was poi, the objects did collide
        poi = mask.overlap(car_mask, offset) 
        return poi

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0

class PlayerCar(AbstractCar): # Inherit from AbstractCar
    IMG = RED_CAR
    START_POS = (400, 450)

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


def draw(win, images, player_car):
    for img, pos in images:
        # Draw this img in this position
        win.blit(img, pos)  
    
    player_car.draw(win)
    
    # Update the window with everything we have drawn
    pygame.display.update() 

def move_player(player_car):
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a]:
        player_car.rotate(left = True)
    if keys[pygame.K_d]:
        player_car.rotate(right = True)
    if keys[pygame.K_w]:
        # While pressing Gas we do not want to slow
        moved = True 
        player_car.move_forward()
    if keys[pygame.K_s]:
        moved = True 
        player_car.move_backward()

    if not moved:
        player_car.reduce_speed()

def handle_collision(player_car):
    # Check if the player car is colliding with the track walls
    if player_car.collide(SCENE_MASK) != None:
        player_car.bounce()


running = True
images = [(SCENE, (0,0))]

player_car = PlayerCar(2,2)


# Main event loop - keeps the game alive
while running:
    # Limit our window to this max speed
    clock.tick(FPS)   

    draw(WIN, images, player_car)

    for event in pygame.event.get():
        # If player clicked X on the window
        if event.type == pygame.QUIT:   
            running = False
            break  

    move_player(player_car)
    handle_collision(player_car)

pygame.quit()   # Close the game cleanly