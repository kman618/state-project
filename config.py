from game_utitilies import scale_images, rotate_center_img, center_text
import pygame as py
from main import window
#set game window
window_x = 1200
window_y = 800
windowsize = (1200,800)
window_scale_x = window_x / 700
window_scale_y = window_y / 500

BACKGROUND = py.transform.scale(py.image.load("background_L1.jpg"), windowsize)
SWAP_BACKGROUND = py.transform.scale(py.image.load("background2.jpg"), windowsize)
CAR1 = scale_images(py.image.load("track_car1.png"), 1)
CAR1 = py.transform.scale(CAR1, (CAR1.get_width() * window_scale_x, CAR1.get_height() * window_scale_y))
CAR2 = scale_images(py.image.load("track_car2.png"), 1)
CAR2 = py.transform.scale(CAR2, (CAR2.get_width() * window_scale_x, CAR2.get_height() * window_scale_y))
LIZARDCAR = scale_images(py.image.load("lizard_car.png"), 1)
LIZARDCAR = py.transform.scale(LIZARDCAR, (LIZARDCAR.get_width() * window_scale_x, LIZARDCAR.get_height() * window_scale_y))
TRACKBORDER = scale_images(py.image.load("track_border.png"), 1)
TRACKBORDER = py.transform.scale(TRACKBORDER, (TRACKBORDER.get_width() * window_scale_x, TRACKBORDER.get_height() * window_scale_y))
TRACKBORDER_MASK = py.mask.from_surface(TRACKBORDER)
TRACK2BORDER = py.image.load("level_two.png")
TRACK2BORDER = py.transform.scale(TRACK2BORDER, (TRACK2BORDER.get_width() * window_scale_x, TRACK2BORDER.get_height() * window_scale_y))
TRACK2BORDER_MASK = py.mask.from_surface(TRACK2BORDER)
RACETRACKL2 = scale_images(py.image.load("race_track_two.png"), 2)
RACETRACKL2 = py.transform.scale(RACETRACKL2, (RACETRACKL2.get_width() * window_scale_x, RACETRACKL2.get_height() * window_scale_y))
RACETRACK = scale_images(py.image.load("track.png"), 1)
RACETRACK = py.transform.scale(RACETRACK, (RACETRACK.get_width() * window_scale_x, RACETRACK.get_height() * window_scale_y))
FINISH =  py.transform.scale(py.image.load("finish_line.png"), (400 * window_scale_x, 50 * window_scale_y))
TRACKBORDER3 = py.image.load("track_border_3.png")
TRACKBORDER3 = py.transform.scale(TRACKBORDER3, (TRACKBORDER3.get_width() * window_scale_x * 2, TRACKBORDER3.get_height() * window_scale_y * 2))
TRACKBORDER3 = scale_images(TRACKBORDER3, .3)
TRACKBORDER3_MASK = py.mask.from_surface(TRACKBORDER3)
RACETRACKL3 = py.image.load("track_3.png")
RACETRACKL3 = py.transform.scale(RACETRACKL3, (RACETRACKL3.get_width() * window_scale_x * 2, RACETRACKL3.get_height() * window_scale_y * 2))
RACETRACKL3 = scale_images(RACETRACKL3, .3)
FINISHMASK = py.mask.from_surface(FINISH)

images = []
images.append(BACKGROUND)
font = py.font.SysFont("comicsans", int(36 * window_scale_x))
fontmedium = py.font.SysFont("comicsans", int(22 * window_scale_x))
fontsmall = py.font.SysFont("comicsans", int(16 * window_scale_x))

half_width = window.get_width()/2
half_height = window.get_height()/2
car_button_x_placement = half_width - (100 * window_scale_y)
WHITE = (255,255,255)