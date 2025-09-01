# Ngā Taonga o Māui (The Treasures of Māui)
# GAME VERSION 1.6
# AUTHOR: Derek WU
# Date: 2025/08/25
# Player/Movement
import pygame
from main_asset import load_character_assets

# Initialize Pygame and display
pygame.init()
screen = pygame.display.set_mode((800, 600)) 

# Load assets (Characters)
maui_right_run, maui_left_run, maui_right_idle,maui_left_idle = load_character_assets()

class Player(pygame.sprite.Sprite):


    def __init__(self, pos): 
        super().__init__()
        
        # Imports palyer graphics from main_asset.py
        self.maui_right_run = maui_right_run
        self.maui_left_run = maui_left_run
        self.maui_right_idle = maui_right_idle
        self.maui_left_idle = maui_left_idle
        self.player_state = self.maui_right_idle # print the maui/player into the game.
        self.image = self.player_state
        self.rect= self.image.get_rect(topleft = pos)
        
        # Player Movement
        self.direction = pygame.math.Vector2(0,0) #Vector stores x and y values in a list
        self.speed = 7
        self.gravity = 0.6
        self.jump_speed = -14
        self.jump_true = True # Stop a lot of jumping in the game


    def get_input(self):  # Handles keyboard input for movement and jumping
        keys = pygame.key.get_pressed()  # Get the current state of all keys

        # Horizontal movement (Right)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.image = self.maui_right_run

        # Horizontal movement (Left)
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.image = self.maui_left_run

        else:  # No horizontal movement
            self.direction.x = 0

        # Jumping
        if self.jump_true:
            if keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]:
                self.jump()  # Apply upward force
                self.jump_true = False  # Prevent double jumping


    def apply_gravity(self): # Have gravity to the character
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
    def jump(self):
        self.direction.y = self.jump_speed  # Negative value to move upward
    def update(self):
        self.get_input() # Find player input
       
