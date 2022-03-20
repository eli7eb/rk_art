# tile class
# all tile properties
# import pygame
# from pygame.locals import *

# # pygame.sprite.Sprite#
class Tile():
    def __init__(self, j, i, crop_tile, texture, k_image, counter_displayed, status, mouse_hover):
        #self.transparant_image = transparant_image
        self.tile_x = j
        self.tile_y = i
        self.crop_tile = crop_tile
        self.texture = texture
        self.k_image = k_image
        self.counter_displayed = counter_displayed
        self.status = status
        self.mouse_hover = mouse_hover
