# GAME VERSION 1.4
# AUTHOR: Derek WU
# Date: 2025/08/11
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
        
        # Player Movement
        self.direction = pygame.math.Vector2(0,0) #Vector stores x and y values in a list
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16
        self.jump_true = True # Stop a lot of jumping in the game


    def get_input (self): # Handles keyboard input for movement and jumping
        keys = pygame.key.get_pressed() # Get the current state of all keys
        
        if keys[pygame.K_RIGHT]: # If the right arrow key is pressed
            self.direction.x = 1
            self.image = self.maui_right_run
            

        elif keys[pygame.K_LEFT]: # If the left arrow key is pressed
            self.direction.x = -1
            self.image = self.maui_left_run

        else: # No keys are pressed stop horizontal movement
            self.direction.x = 0

        if self.jump_true:   # Jumping 
            if keys[pygame.K_UP]: 
                self.jump() # Have Upward force
                self.jump_true = False # Stop double jumping


    def apply_gravity(self): # Have gravity to the character
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
    def jump(self):
        self.direction.y = self.jump_speed  # Negative value to move upward
    def update(self):
        self.get_input() # Find player input
       
