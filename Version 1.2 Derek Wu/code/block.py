# GAME VERSION 1.2
# AUTHOR: Derek WU
# Date: 2025/07/28
# block.py
import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,image_type):
        super().__init__()

        #Load tiles images
        self.grass_block_img =  pygame.image.load('graphics/grass_block.png').convert_alpha()
        self.dirt_block_img = pygame.image.load('graphics/dirt_block.png').convert_alpha()
        
        if image_type == 'dirt':
            self.image = self.dirt_block_img
        if image_type == 'grass':
            self.image = self.grass_block_img 
        self.rect = self.image.get_rect(topleft = pos)
        
    def update(self, x_shift):
        self.rect.x += x_shift  #moves tiles to left or right accordinly to player movement
