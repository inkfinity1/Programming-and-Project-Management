# Ngā Taonga o Māui (The Treasures of Māui)
# GAME VERSION 1.6
# AUTHOR: Derek WU
# Date: 2025/08/25
# Map/tiles

import pygame
from main_asset import load_block_assets

# Initialize Pygame and display
pygame.init()
screen = pygame.display.set_mode((800, 600)) 

#Load block from main_asset.py
grass_block_img, dirt_block_img, kiwi_block_img = load_block_assets ()

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,image_type):
        super().__init__()

        #Load tiles images
        self.grass_block_img = grass_block_img
        self.dirt_block_img = dirt_block_img
        self.kiwi_block_img = kiwi_block_img

        if image_type == 'dirt':
            self.image = self.dirt_block_img
        if image_type == 'grass':
            self.image = self.grass_block_img 
        if image_type == 'kiwi':
            self.image = self.kiwi_block_img 
        
        self.rect = self.image.get_rect(topleft = pos)
        
    def update(self, x_shift):
        self.rect.x += x_shift  #moves tiles to left or right accordinly to player movement


# level 1 map

level_map_1 = [

'                                                                                 ',
'                                                                                 ',
' G P                            U                                                ',
' DGGG                         GGG                           G   GG               ',
'  DDD                   GG  G U DG      GGG           GG        DD   GG  TTT     ',
'  DDD GG      GG  GG   GD    DDDDDDGG   DDD        GG                            ',
'        GG  G                 DDDD            GG   DD                            ']

#level 2
level_map_2 = [
'                                                                               ',
'                                                                               ',
'G P                                                                            ',
'DGGG                     GG                             G                   ',
' DDDU        U   GG    GDDDU      GGGU      GGG  GG          GG    TTTTT   ',
' DDDG      GGGG  DD    GGDDDGG   GG DDDGG                UG           D      ',
'         GG                  DDDD   DD                  GGDG                ']

#level 3
level_map_3 = [
'                                                                            ',
'                                                   G                        ',
'G P                                               GDDD                      ',
'DGGG         GGG                           U    G      GGGU   GGGU          ',
' DDDU   GGGU DD       U          UGGG    GGGGG  D         DG    DG          ',
' DDDG    DU GG     GGGGGG    GGGGGDDD    DDDDD            DG        GG  GGTT',
'         DDDD        DD      DDDDDDD      DDD                          DDDD ']


#level 4
level_map_4 = [

'            ',
'         ',
'                                                                                                             ',
'                                                                                                     GGTTT  ',
'G  P                                                                                           GG              ', 
'DGGG                                                                      U        U     GGG                   ',
' DDD     U      U    U      U     U      U      U         U      U    GGGGGGG    GGGGG   DDD                   ',
' DDDGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGDDDDDDD    DDDDD                         ']

tile_size = 60
screen_width = 800
screen_height = max(len(level_map_1), len(level_map_2), len(level_map_3), len(level_map_4)) * tile_size

