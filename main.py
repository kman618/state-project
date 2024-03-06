import pygame as py 
import random as r
import time
import math as m
#import necissary functions from game_utilities folder
from game_utitilies import scale_images, rotate_center_img, center_text
py.init()
py.font.init()

#load and scale images 

BACKGROUND = scale_images(py.image.load("background_L1.jpg"), .3)
SWAP_BACKGROUND = scale_images(py.image.load("background2.jpg"), .15)
CAR1 = scale_images(py.image.load("track_car1.png"), 1)
CAR2 = scale_images(py.image.load("track_car2.png"), 1)
LIZARDCAR = scale_images(py.image.load("lizard_car.png"), 1)
TRACKBORDER = scale_images(py.image.load("track_border.png"), 1)
TRACKBORDER_MASK = py.mask.from_surface(TRACKBORDER)
TRACK2BORDER = py.image.load("level_two.png")
TRACK2BORDER_MASK = py.mask.from_surface(TRACK2BORDER)
RACETRACKL2 = scale_images(py.image.load("race_track_two.png"), 1)
RACETRACK = scale_images(py.image.load("track.png"), 1)
FINISH =  py.transform.scale(py.image.load("finish_line.png"), (400, 50))
FINISHMASK = py.mask.from_surface(FINISH)
#set game window
windowsize = (700,500)
window = py.display.set_mode(windowsize)
done = False
clock = py.time.Clock()
fps = 60
images = []
images.append(BACKGROUND)
font = py.font.SysFont("comicsans", 36)
fontmedium = py.font.SysFont("comicsans", 22)
fontsmall = py.font.SysFont("comicsans", 16)

#-----------------------------------------------------------------------[]
#CLASSES
#-----------------------------------------------------------------------[]

class Finish:
    def __init__(self, img):
        self.img = img
        self.level = 1
        self.x = 375
        self.y = 2360


    def update(self, window):
        window.blit(self.img, (self.x, self.y))
        py.display.update()
    def level_pos(self, level):
        self.level = level
        if self.level == 1:
            self.x = 375
            self.y = 2360
        elif self.level == 2:
            self.x = 645
            self.y = 2255
    
    def shift(self, direction, vel):
        if direction == "U":
            self. y -= vel
        if direction == "D":
            self.y += vel
        if direction == "L":
            self.x += vel
        if direction == "R":
            self.x -= vel


class Track:
    def __init__(self, x, y, track_img):
        
        self.img = track_img
        self.rect = self.img.get_rect()
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y


    def update(self, window):
        window.blit(self.img, (self.x, self.y))
        


    def shift(self, direction, vel):
        if direction == "U":
            self. y -= vel
        if direction == "D":
            self.y += vel
        if direction == "L":
            self.x += vel
        if direction == "R":
            self.x -= vel
        finish_line.shift(direction, vel)

        










#----------------------------------------{}
#buttons class for main menu
class Button:
    def __init__(self, image, x, y, text, grow, ownfont):
        self.image = image
        self.x_pos = x
        self.y_pos = y
        self.text = text
        self.font = ownfont
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_display = self.font.render(self.text, True, (255,255,255))
        self.text_rect = self.text_display.get_rect(center=(self.x_pos, self.y_pos))
        self.clicked = False
        self.grow = grow
        self.image_normal = image
        self.image_grow = scale_images(self.image, 1.2)
        self.hovering = False
    def update(self):
        self.colorShift(py.mouse.get_pos()) #allows you to change the text of the button from user input
        window.blit(self.image, self.rect)
        window.blit(self.text_display, self.text_rect)
    def checkClick(self,position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.clicked = True

    def colorShift(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            if self.grow == True:
                self.image = self.image_grow
            self.text_display = self.font.render(self.text, True, (150,255,150))
            self.hovering = True #Helps with stats dipslay while hovering over a car option
        else:
            self.image = self.image_normal
            self.text_display = self.font.render(self.text, True, (255,255,255))
            self.hovering = False

#--------------------------------------{}

#levels etc.. switch through tracks + difficulty + game stats
class Game_info:
    LEVELS = 10
    def __init__(self, Level=1):
        self.level = Level
        self.level_started = False
        self.level_started_time = 0

    def level_next(self):
        self.level += 1
        self.level_started = False
        self.level_started_time = 0
        finish_line.level_pos(self.level)
        player_one_car.level_reset()
    def reset_levels(self):
        self.level = 1
        self.level_started = False
        self.level_started_time = 0

    def finished(self):
        return self.level > self.LEVELS
    

    def level_start(self):
        self.level_started = True
        finish_line.level_pos(self.level)
        self.level_started_time = time.time()


    def time_in_level(self):
        if self.level_started == False:
            return 0
        return time.time() - self.level_started_time
    
    def redo_level(self, current_track):
        self.level_started = False
        self.level_started_time = 0
        current_track.x = current_track.start_x
        current_track.y = current_track.start_y
        player_one_car.level_reset()

    
#-------------------------{}


#creating an inheritance class for cars to allow computer based track car
class Base_car:
    
    def __init__(self, rotation_V, max_V, starting_pos_x, starting_pos_y, starting_gear, car):
        #vel = velocity = V, setting maxes to allow for individual car stats
        self.car = car
        if self.car == 1:
            self.img = CAR1
        elif self.car == 2:
            self.img  = CAR2
        elif self.car == 3:
            self.img = LIZARDCAR
        self.max_V = max_V
        self.max_D = 2
        #allows for a non linear acceleartion of the car
        self.acc = 0.06
        self.dec = .12
        self.vel = 0
        self.angle = 180
        self.rotation_V = rotation_V
        self.max_rotation_V = 6
        self.rotation_acc = 2
        self.rect = self.img.get_rect()
        self.x = starting_pos_x
        self.y = starting_pos_y
        self.gear = starting_gear
        self.forward = False
        self.reverse = False
        self.drifting = False
        self.car_mask = py.mask.from_surface(self.img)
        self.starting_x = starting_pos_x
        self.starting_y = starting_pos_y
    def level_reset(self):
        self.x = self.starting_x
        self.y = self.starting_y
        self.angle = 180
        self.vel = 0
    #acquire general game stats for car
    def reset(self):
        #updates it to the current car
        self.update()
    def stats(self):
        self.gear = "N"
        if self.reverse == True:
            self.gear = "R"
        elif self.forward == True:
            gear = round(abs(self.vel - 0.5)/2)
            if self.vel < 0:
                gear = -1
            if gear > 0:
                self.gear = str(gear)
            elif gear == 0:
                self.gear = "1"
            elif gear == -1:
                self.gear = "R"
        
        speed = abs(self.vel * 15)
        self.speed = str(round(speed))

    #draws car
    def draw(self, surface):
        
        #find rotation and account for it with hitbox and drawing
        
        rotate_center_img(surface, self.img, (self.x, self.y), self.angle, self)
    #allows for as many cars as you want that the player can choose from
    def update(self):
        if self.car == 1:
            self.img = CAR1
            self.max_V = 10
            self.max_rotation_V = 2.5
            self.acc = .06
            self.max_D = 2
            self.rotation_V = 4
            self.dec = .12
        elif self.car == 2:
            self.img  = CAR2
            self.max_V = 13
            self.max_rotation_V = 2
            self.rotation_V = 3.7
            self.acc = .045
            self.max_D = 3
            self.dec = .09
        elif self.car == 3:
            self.img = LIZARDCAR
            self.max_V = 8
            self.max_rotation_V = 4
            self.rotation_V = 5.5
            self.acc = .1
            self.dec = .035
            self.max_D = 1.1

        
    #allows turning with controllers
    def car_rotation(self, left=False, right=False):
        if self.vel >= .06 or self.vel <= -.15: #prevents the car from turning when not in motion
            self.turn_speed()
            if left == True:
                self.angle += self.rotation_V
            elif right == True:
                self.angle -= self.rotation_V
    def move(self, current_track):
        #finds angular movement using trig and allowes for movement one way in any angle
        #had issues with angles, had to convert to radians
        radians = m.radians(self.angle)
        #switched sin and cos and it fixed the issue
        velX = ((m.sin(radians)) * self.vel)
        velY = ((m.cos(radians)) * self.vel)
        #allows for adding to mask
        self.velX = velX
        self.velY = velY
        #played around and switched to -, radians come back negative sometimes which was no bueno so it was negative, had to play w it
        self.current_track = current_track
        #Shifts track down rather than car up if car is at a certain boundary
        xbound = 320
        ybound = 220
        if self.x - self.velX <= xbound: 
            self.current_track.shift("L", abs(self.velX))
        elif self.x - self.velX >= 700 - xbound:   
            self.current_track.shift("R", abs(self.velX))
        else:
            self.x -= velX
        if self.y - self.velY <= ybound:
            self.current_track.shift("U", -1 * abs(self.velY))
        elif self.y - self.velY >= 500 - ybound:
            self.current_track.shift("D", -1 * abs((self.velY)))
        else:
            self.y -= velY
    #accelerates the car
    def update_forward(self,current_track):
        self.vel = min(self.vel + self.acc, self.max_V)
        self.move(current_track)


    def update_reverse(self, forward, current_track):
        
        if self.vel > 0 + self.dec or self.gear == "R": #keeps it from updating velocity to a negative while stopped if braking in nuetral
            self.vel = max(self.vel - self.dec, -1 * self.max_D)
        if forward == False:
            #makes it so you have to be in reverse to back up, smooths out breakings
            if self.vel <= 0 + self.dec:
                self.stats()
                if self.gear == "R":
                    self.move(current_track)
            elif self.vel > 0 + self.dec:
                self.move(current_track)

    def collide(self, mask, x, y):
        #uses mask with track border to detect collisions
        offsetx = int(self.x - x - 30)
        offsety = int(self.y - y)
        collision = mask.overlap(self.car_mask, (offsetx, offsety))
        return collision
    def finish(self,mask,x,y):
        offsetx = int(self.x - x)
        offsety = int(self.y - y)
        collision_finish = mask.overlap(self.car_mask, (offsetx, offsety))
        return collision_finish
    

    def turn_speed(self):
        #turning radius is determined by speed, prevents unrealistic turning manuevers
        self.rotation_V = min(self.vel/self.rotation_acc  , self.max_rotation_V)
    """
    def drift(self):
        self.max_rotation_V = 8
        self.rotation_acc = 1.5 * self.drift_boost #sharper turning while drifting, sharper turning the longer youve drifted for
        self.max_V = 7 * self.drift_boost
        self.acc = 0.04 * self.drift_boost
    """

#--------------------------------------------{}

#Use the parent class to create the player cars
class User_car(Base_car):
    starting_pos_x = 200
    starting_pos_y = 200
    starting_gear = "N"
    #allows the car to slow down when you let off the gass
    def update_slow(self, current_track):
        player_one_car.forward = False
        if self.vel > 0:
            self.vel = max(self.vel - self.acc/1.5, 0)
        elif self.vel < 0:
            self.vel = min(self.vel + self.acc/1, 0)
        self.move(current_track)
    def bounce(self, current_track):
        if self.vel < 0:
            min_vel = 1
        else:
            min_vel = -1
        self.vel = min(-self.vel/3, min_vel)
        self.move(current_track)

#-------------------------------------------------{}

#cpu car/ multiplayer car
class Opponent_car(Base_car):
    IMAGE = CAR2
    starting_pos_x = 400
    starting_pos_y = 400





#-----------()
#variables for commonly used things
half_width = window.get_width()/2
half_height = window.get_height()/2
car_button_x_placement = half_width - 100
WHITE = (255,255,255)
#--------------------------------------------------------------------------[]
#OBJECTS
#--------------------------------------------------------------------------[]
player_one_car = User_car(4, 10, half_width, half_height, "N", 1)
player_one_car.stats()
cpu_car = Opponent_car(5,3.5, 400,400, "N", 2)
#game class into object
game_info = Game_info()

#button objects
#main screen buttons
play_button_img = py.image.load("play_button.png")
play_button = Button(play_button_img, half_width, window.get_height()/2.4, "PLAY", False, font)
car_button_img = py.image.load("change_cars.png")
car_button = Button(car_button_img, half_width, window.get_height()/ 1.5 + 60, "SWAP CAR", False, font)
instructions_button_img = py.image.load("instructions_button.png")
instructions_button = Button(instructions_button_img, half_width, window.get_height()/1.68, "Instructions", False, font)
#---------------------- car 1
car1_button_img = py.image.load("track_car1.png")
car1_button_img = py.transform.rotate(car1_button_img, 90)
car1_button = Button(car1_button_img, car_button_x_placement, window.get_height()/3, "", True, font)
#----------------------- car 2
car2_button_img = py.image.load("track_car2.png")
car2_button_img = py.transform.rotate(car2_button_img, 90)
car2_button = Button(car2_button_img, car_button_x_placement, half_height, "", True, font)
#----------------------- car 3
car3_button_img = py.image.load("lizard_car.png")
car3_button_img = py.transform.rotate(car3_button_img, 90)
car3_button = Button(car3_button_img, car_button_x_placement, window.get_height()/ 1.5, "", True, font)

#------ menu functionality buttons
close_button_img = py.image.load("close_button.png")
close_button_img = scale_images(close_button_img, .8)
close_button = Button(close_button_img, 65,65, "", True, font)
instructions_screen_img = py.image.load("instructions_screen.png")
instructions_screen_img = scale_images(instructions_screen_img, .65)
instructions_screen_button = Button(instructions_screen_img, half_width, half_height, "", False, font)
blank_button_img = py.image.load("blank_button.png")
next_button = Button(blank_button_img, half_width + 100, half_height + 100, "NEXT LEVEL", False, fontsmall)
redo_level_button = Button(blank_button_img, half_width - 100, half_height + 100, "RETRY", False, fontmedium)

#LEVEL TRACK OBJECTS
track_one = Track(150, 25, RACETRACK)
track_two = Track(150,25, RACETRACKL2)
finish_line = Finish(FINISH)
#------------------------------------------[gear text base font render]
#GEAR STATS, GAME STATS, RENDER
gear_text = font.render('[G: ' + player_one_car.gear + "MPH: " + player_one_car.speed + " L: " + str(game_info.level) + "]", True, WHITE)





#-----------------------------------------------------------------------[]
#FUNCTIONS
#-----------------------------------------------------------------------[]
#functions for cleaner code
def drawing(surface, player_car, track):
    track.update(window)
    player_car.draw(surface)
    surface.blit(gear_text, ((surface.get_width() - gear_text.get_width() - 15), 10))
    

#------------------------------------------{}
def move_player(player_car, current_track):
    #gather keys currently pressed out of event loop so they run every tick
    keys = py.key.get_pressed()
    moving = False
    forward = False
    reverse = False
    player_car.forward = False
    player_car.drifting = False
    if keys[py.K_a]:
        player_car.car_rotation(left=True)
    if keys[py.K_d]:
        player_car.car_rotation(right=True)
    if keys[py.K_w]:
        moving = True
        forward = True
        player_car.forward = True
        player_car.reverse = False
        player_car.update_forward(current_track)
    if keys[py.K_LSHIFT]:
        #reverse/ braking
        moving = True
        reverse = True
        player_car.update_reverse(forward,current_track)
    if keys[py.K_SPACE]:
        #Drifting Mechanic
        #player_car.drift()
        player_car.drifting = True
    #deceleration when not accelerating or boosting
    if moving == False:
        player_car.update_slow(current_track)

#--------------------------------------{}
#main game loop in a function to allow multiple main game loops for a menu screen
def main_game_loop():
    done = False
    finish_line.update(window)
    global main_menu_run
    if game_info.level == 1:
        current_track = track_one
    elif game_info.level == 2:
        current_track = track_two
    player_one_car.level_reset()
    while not done:
        player_one_car.update()
        window.fill((0,0 ,0))
        
        global gear_text
        player_one_car.forward = False
        if player_one_car.drifting == False:
            player_one_car.reset()
        player_one_car.reset()
        clock.tick(fps)
        #game logic above, drawing below
        #added all drawing to the drawing function for polished code
        move_player(player_one_car, current_track)
        player_one_car.stats()
        #update stat texts
        gear_text = font.render('[G: ' + player_one_car.gear + "  MPH: " + player_one_car.speed + "  L: " + str(game_info.level) + " T: " + str(abs(round(game_info.time_in_level()))) + "]", True, WHITE)
        #initiate main draw function

        if game_info.level == 1:
            current_track = track_one
        elif game_info.level == 2:
            current_track = track_two
        drawing(window, player_one_car, current_track)
        finish_line.update(window)
        py.display.update()
        #cpu_car.draw(window)
        #py.display.flip()
        #main event loop
        while not game_info.level_started:
            center_text(window, font, f"Press any key to intitiate race {game_info.level}")
            py.display.update()
            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                if event.type == py.KEYDOWN:
                    game_info.level_start()


        for event in py.event.get():
            if event.type == py.QUIT:
                done = True
                py.quit()
            if event.type == py.KEYDOWN:
                if event.key == py.K_r:
                #allows you to put the car into reverse when at a stands still
                    player_one_car.stats()
                    if player_one_car.gear == "N" and player_one_car.vel <= .5:
                        player_one_car.gear == "R"
                        player_one_car.reverse = True
                if event.key == py.K_m:
                    main_menu_run = True
                    done = True
                if event.key == py.K_n:
                    game_info.level_next()
                    if game_info.level == 1:
                        current_track = track_one
                    elif game_info.level == 2:
                        current_track = track_two
        
        if game_info.level == 1:
            current_track = track_one
            if player_one_car.collide(TRACKBORDER_MASK, current_track.x, current_track.y) != None:
                player_one_car.bounce(current_track)
            
        elif game_info.level == 2:
            current_track = track_two
            if player_one_car.collide(TRACK2BORDER_MASK, current_track.x, current_track.y) != None:
                player_one_car.bounce(current_track)
        if player_one_car.collide(FINISHMASK, finish_line.x, finish_line.y) != None:
            # build a menu for finish  =finish()
            level_end_screen()
        
#-------------------------------{}
#original menu while loop
def main_menu():
    global main_menu_run
    global change_cars_run
    done = False
    while not done:
        #resetting them inside the main while loop unlike the others because they stay within this function the entire time
        instructions_screen_button.clicked = False
        instructions_button.clicked = False 
        

        window.fill((0,0,0))
        window.blit(BACKGROUND, (0,0))
        #hover or click 
        mouse_position = py.mouse.get_pos()
        #displays menu text
        m_text = font.render("Main Menu", True, (WHITE))
        m_rect = m_text.get_rect(center=(window.get_width()/2, window.get_height()/4))
        main_menu_background = py.image.load("main_menu_background.png")
        main_menu_background = py.transform.scale(main_menu_background, (350, 450))
        main_menu_background_rect = main_menu_background.get_rect(center=(window.get_width()/2, window.get_height()/2))
        window.blit(main_menu_background, main_menu_background_rect)
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()

            if event.type == py.MOUSEBUTTONDOWN and event.button == 1:
                play_button.checkClick(py.mouse.get_pos())
                car_button.checkClick(py.mouse.get_pos())
                instructions_button.checkClick(py.mouse.get_pos())




        #buttons 
        play_button.update()
        car_button.update()
        instructions_button.update()
        play_button.colorShift(py.mouse.get_pos())
        car_button.colorShift(py.mouse.get_pos())
        instructions_button.colorShift(py.mouse.get_pos())

        window.blit(m_text, m_rect)
        py.display.update()
        
        if play_button.clicked == True:
            done = True
            main_menu_run = False
        if car_button.clicked == True:
            done = True
            main_menu_run = False
            change_cars_run = True

        # Runs a seperate instruction menu screen on top of partial screen, if you click out it goes away.
        if instructions_button.clicked == True:
            run_instruct = True
            while run_instruct:
                instructions_screen_button.clicked = False
                for event in py.event.get():
                    if event.type == py.QUIT:
                        py.quit()

                    if event.type == py.MOUSEBUTTONDOWN and event.button == 1:
                        instructions_screen_button.checkClick(py.mouse.get_pos())
                        if instructions_screen_button.clicked == False:
                            run_instruct  = False
                instructions_screen_button.update()
                py.display.update()
        
                
                



#functions for swap car menu specifically
#--------------------------------------------{}
def reset_car_button(car_button):
    car_button.text = ""
    car_button.text_rect = car_button.text_display.get_rect(center=(car_button.x_pos, car_button.y_pos))
#cleans up main function by putting large code into function
def hover_text_display(car_button):
    if car_button == 1:
        car1_info_text_s = font.render("Speed: 10", True, WHITE)
        car1_info_text_S_rect = car1_info_text_s.get_rect(center=(car1_button.x_pos + 175, car1_button.y_pos))
        car1_info_text_a = font.render("Acceleration: 6", True, WHITE)
        car1_info_text_A_rect = car1_info_text_s.get_rect(center=(car1_button.x_pos + 175, car1_button.y_pos + 35))
        car1_info_text_t = font.render("Turning: 4", True, WHITE)
        car1_info_text_T_rect = car1_info_text_s.get_rect(center=(car1_button.x_pos + 175, car1_button.y_pos + 70))
        window.blit(car1_info_text_s, car1_info_text_S_rect)
        window.blit(car1_info_text_a, car1_info_text_A_rect)
        window.blit(car1_info_text_t, car1_info_text_T_rect)
    elif car_button == 2:
        car2_info_text_s = font.render("Speed: 12", True, WHITE)
        car2_info_text_a = font.render("Acceleration: 4.5", True, WHITE)
        car2_info_text_t = font.render("Turning: 3.75", True, WHITE)
        car2_info_text_S_rect = car2_info_text_s.get_rect(center=(car2_button.x_pos + 175, car2_button.y_pos))
        car2_info_text_A_rect = car2_info_text_s.get_rect(center=(car2_button.x_pos + 175, car2_button.y_pos + 35))
        car2_info_text_T_rect = car2_info_text_s.get_rect(center=(car2_button.x_pos + 175, car2_button.y_pos + 70))
        window.blit(car2_info_text_s, car2_info_text_S_rect)
        window.blit(car2_info_text_a, car2_info_text_A_rect)
        window.blit(car2_info_text_t, car2_info_text_T_rect)
    elif car_button == 3:
        car3_info_text_s = font.render("Speed: 8", True, WHITE)
        car3_info_text_a = font.render("Acceleration: 10", True, WHITE)
        car3_info_text_t = font.render("Turning: 5.5", True, WHITE)
        car3_info_text_special = font.render("Special: Sticky Hook", True, WHITE)
        car3_info_text_S_rect = car3_info_text_s.get_rect(center=(car3_button.x_pos + 175, car3_button.y_pos))
        car3_info_text_A_rect = car3_info_text_s.get_rect(center=(car3_button.x_pos + 175, car3_button.y_pos + 35))
        car3_info_text_T_rect = car3_info_text_s.get_rect(center=(car3_button.x_pos + 175, car3_button.y_pos + 70))
        car3_info_text_Special_rect = car3_info_text_s.get_rect(center=(car3_button.x_pos + 175, car3_button.y_pos + 105))
        window.blit(car3_info_text_s, car3_info_text_S_rect)
        window.blit(car3_info_text_a, car3_info_text_A_rect)
        window.blit(car3_info_text_t, car3_info_text_T_rect)
        window.blit(car3_info_text_special, car3_info_text_Special_rect)
#--- swap cars menu
            
def swap_cars_menu(current_car):
    done = False
    global change_cars_run
    global main_menu_run
    while not done:
        #next 4 lines allow it to be reopened without automatically selecting a car or instantly closing because its stuck on a button alr being clicked. 
        car2_button.clicked = False
        car1_button.clicked = False
        car3_button.clicked = False
        close_button.clicked = False
        change_cars_run = True
        if current_car == 1:
            car1_button.text = "Current:"
            car1_button.text_rect = car1_button.text_display.get_rect(center=(car1_button.x_pos -150, car1_button.y_pos))
            reset_car_button(car2_button)
            reset_car_button(car3_button)
        elif current_car == 2:
            car2_button.text = "Current:"
            car2_button.text_rect = car2_button.text_display.get_rect(center=(car2_button.x_pos -150, car2_button.y_pos))
            reset_car_button(car1_button)
            reset_car_button(car3_button)
        elif current_car == 3:
            car3_button.text = "Current:"
            car3_button.text_rect = car3_button.text_display.get_rect(center=(car3_button.x_pos -150, car3_button.y_pos))
            reset_car_button(car1_button)
            reset_car_button(car2_button)
        else:
            reset_car_button(car1_button)
            reset_car_button(car2_button)
            reset_car_button(car3_button)

        window.fill((0,0,0))
        window.blit(SWAP_BACKGROUND, (0,0))
        #main caption text for screen
        c_text = font.render("Swap Car", True, (WHITE))
        c_rect = c_text.get_rect(center=(window.get_width()/2, window.get_height()/5.5))

        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
            if event.type == py.MOUSEBUTTONDOWN and event.button == 1:
                car1_button.checkClick(py.mouse.get_pos())
                car2_button.checkClick(py.mouse.get_pos())
                car3_button.checkClick(py.mouse.get_pos())
                close_button.checkClick(py.mouse.get_pos())
        car1_button.update()
        car1_button.colorShift(py.mouse.get_pos())
        car2_button.update()
        car2_button.colorShift(py.mouse.get_pos())
        car3_button.update()
        car3_button.colorShift(py.mouse.get_pos())
        close_button.update()
        close_button.colorShift(py.mouse.get_pos())
        window.blit(c_text, c_rect)
        if car1_button.hovering == True:
            hover_text_display(1)
        elif car2_button.hovering == True:
            hover_text_display(2)
        elif car3_button.hovering == True:
            hover_text_display(3)
        #checks if car was clicked, and then updates main playing car and which car is current in the display screen
        if car1_button.clicked == True:
            player_one_car.car = 1
            current_car = 1
        elif car2_button.clicked == True:
            player_one_car.car = 2
            current_car = 2
        elif car3_button.clicked == True:
            player_one_car.car = 3
            current_car = 3
        if close_button.clicked == True: #closes the swap car menu and re-opens the main menu
            change_cars_run = False
            done = True
            main_menu_run = True
        
        py.display.update()

def level_end_screen():
    #secondary screen for when a level is complete so it doesnt immedietly jump to the next level. 
    done = False
    global change_cars_run
    global main_menu_run
    print(game_info.level)
    if game_info.level == 1:
        current_track = track_one
    elif game_info.level == 2:
        current_track = track_two
    next_button.clicked = False
    redo_level_button.clicked = False
    while not done:
        window.fill((0,0,0))
        
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
            if event.type == py.MOUSEBUTTONDOWN and event.button == 1:
                next_button.checkClick(py.mouse.get_pos())
                redo_level_button.checkClick(py.mouse.get_pos())

        next_button.update()
        next_button.colorShift(py.mouse.get_pos())
        redo_level_button.update()
        redo_level_button.colorShift(py.mouse.get_pos())

        if next_button.clicked == True:
            done = True
            game_info.level_next()
        elif redo_level_button.clicked == True:
            done = True
            #reset level
            game_info.redo_level(current_track)
            finish_line.level_pos(game_info.level)
        py.display.update()

player_one_car.reverse = False #little failsafe






#-----------------------------------------------------------------------[]
#EVENT LOOP
#-----------------------------------------------------------------------[]


#main game loop below 

main_menu_run = True #allows main menu to be re-opened mid game
change_cars_run = False
while not done:
    while main_menu_run == True or change_cars_run == True:
        if main_menu_run == True:
            play_button.clicked = False
            main_menu()
        if change_cars_run == True:
            car_button.clicked = False
            swap_cars_menu(player_one_car.car)
        
    track_one.x = 150
    track_one.y = 25
    player_one_car.level_reset()
    main_game_loop()

    

py.quit()

#--------------------------------------------------[]
#CURRENT BUGS
#--------------------------------------------------[]
"""
2: Car sometimes gets stuck in a collision zone and is contantly colliding making it impossible to drive the car
"""












