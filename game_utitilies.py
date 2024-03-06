import pygame as py
#text on center of screen
def center_text(surface, font, text):
    render = font.render(text, 1, (255, 0,0))
    surface.blit(render, ((surface.get_width()/2 - render.get_width()/2), surface.get_height()/2 - render.get_height()/2 - 35))
#scales images easily
def scale_images(image, scale):
    new_size_w = round(image.get_width() * scale)
    new_size_h = round(image.get_height() * scale)
    return py.transform.scale(image, (new_size_w, new_size_h))
#allows for the rotation of images, primarily the vehicle, around the center instead of the default top left coordinate 
def rotate_center_img(surface, image, top_left, angle, vehicle):
    rect = image.get_rect(topleft = top_left)
    new_rotate = py.transform.rotate(image, angle)
    #keeps rect the same without skewing image
    new_center_rect = new_rotate.get_rect(center = rect.center)
    surface.blit(new_rotate, new_center_rect.topleft)
    vehicle.car_mask = py.mask.from_surface(new_rotate)

    