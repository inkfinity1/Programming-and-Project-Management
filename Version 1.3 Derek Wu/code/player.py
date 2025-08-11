# GAME VERSION 1.3
# AUTHOR: Derek WU
# Date: 2025/08/04
import pygame
from main_asset import load_character_assets

# Initialize Pygame and display
pygame.init()
screen = pygame.display.set_mode((800, 600)) 

# Load assets (Characters)
maui_right_run, maui_left_run, maui_right_idle = load_character_assets()

class Player(pygame.sprite.Sprite):


    def __init__(self, pos): 
        super().__init__()
        
        # Imports palyer graphics from main_asset.py
        self.maui_right_run = maui_right_run
        self.maui_left_run = maui_left_run
        self.maui_right_idle = maui_right_idle
        self.player_state = self.maui_right_idle # print the maui/player into the game.
        self.image = self.player_state
        self.rect= self.image.get_rect(topleft = pos)
        



    