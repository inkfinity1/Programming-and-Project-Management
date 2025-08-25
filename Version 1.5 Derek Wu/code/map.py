# Ngā Taonga o Māui (The Treasures of Māui)
# GAME VERSION 1.5
# AUTHOR: Derek WU
# Date: 2025/08/18

import pygame
from main_asset import load_block_assets

# Initialize Pygame and display
pygame.init()
screen = pygame.display.set_mode((800, 600)) 

#Load block from main_asset.py
grass_block_img, dirt_block_img = load_block_assets ()

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,image_type):
        super().__init__()

        #Load tiles images
        self.grass_block_img = grass_block_img
        self.dirt_block_img = dirt_block_img
        if image_type == 'dirt':
            self.image = self.dirt_block_img
        if image_type == 'grass':
            self.image = self.grass_block_img 
        self.rect = self.image.get_rect(topleft = pos)
        
    def update(self, x_shift):
        self.rect.x += x_shift  #moves tiles to left or right accordinly to player movement


# level 1 map

level_map_1 = [

'                                                                                 ',
'                                                                                 ',
' G P                                                                             ',
' DGG                         GGGG                 GGGG         GGGGGG            ',
'  DD                   GG    DDDD       GGG       DDDD GG   GG DDDDDD   GG  TTT  ',
'  DDG  GG      GG  GG  DD    DDDDGGGG   DDD GGG        DDG                  D    ',
'        GG   DD                DDDD                  DDD                         ']

#level 2
level_map_2 = [
'                                                                               ',
'                                                                               ',
'                                                                               ',
'GG                         GGGG                 GGGG         GGGGGG            ',
'DD    P               GG    DDDD       GGG       DDDD GG   GG DDDDDD   G TTTTT ',
'DDG  GG      G  G  DD    DDDDGGGG   DDD GGG        DDG                  D    ',
'        GG                  DDDD                  DDD                       ']

#level 3
level_map_3 = [
'                                                                               ',
'                                                                               ',
'                                                                               ',
'GG                         GGGG                 GGGG         GGGGGG            ',
'DD    P               GG    DDDD       GGG       DDDD GG   GG DDDDDD   G TTTTT ',
'DDG  GG      GG  GG  DD    DDDDGGGG   DDD GGG        DDG                  D    ',
'        GG   DD                DDDD                  DDD                       ']
tile_size = 60
screen_width = 800
screen_height = max(len(level_map_1), len(level_map_2), len(level_map_3)) * tile_size

