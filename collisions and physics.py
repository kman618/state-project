import pygame as py 
import random as r
import time
import math as m
#import necissary functions from game_utilities folder
from game_utitilies import scale_images, rotate_center_img, center_text
py.init()
py.font.init()

# class Track(self, )

class Car(py.sprite.Sprite):
    def __init__(self, rotation_V, max_V, starting_pos_x, starting_pos_y, img):
        py.sprite.Sprite.__init__(self)
        self.image = img
        # self.turning_center = None
        # self.center_of_mass = 