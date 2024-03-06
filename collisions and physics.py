import pygame as py 
import random as r
import time
import math as m
#import necissary functions from game_utilities folder
from game_utitilies import scale_images, rotate_center_img, center_text
py.init()
py.font.init()

# class Track(self, )

# class Car(py.sprite.Sprite):
#     def __init__(self, rotation_V, max_V, starting_pos_x, starting_pos_y, img):
#         py.sprite.Sprite.__init__(self)
#         self.image = img
#         # self.turning_center = None
#         # self.center_of_mass = 
class PhysicsObject(py.sprite.Sprite):
    def __init__(self, image: py.Surface, center_of_mass: tuple = None, density: float = 1):
        py.sprite.Sprite.__init__(self)
        self.image = image
        self.mask = py.mask.from_surface(self.image)
        self.density = density
        self.mass = self.density * self.mask.count()
        self.center_of_mass = center_of_mass
        self.x, self.y, self.dx, self.dy = 0, 0, 0, 0
        self.angle, self.angular_velocity = 0, 0

# class Car(PhysicsObject):
    # def __init__(self, *)