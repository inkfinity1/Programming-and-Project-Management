
       
# Ngā Taonga o Māui (The Treasures of Māui)
# GAME VERSION 1.7
# AUTHOR: Derek WU
# Date: 2025/09/01
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

        # Animation frames
        self.maui_right_run = [maui_right_idle, maui_right_run, maui_right_idle]
        self.maui_left_run = [maui_left_idle, maui_left_run, maui_left_idle]
        self.maui_left_idle = [maui_left_idle]
        self.maui_right_idle = [maui_right_idle]
        # Animation state
        self.facing_right = True
        self.frame_index = 0
        self.animation_speed = 0.09
        self.image = self.maui_right_idle[0]
        self.rect = self.image.get_rect(topleft=pos)

        # Maui/User/Player Movement
        self.direction = pygame.math.Vector2(0,0) #Vector stores x and y values in a list
        self.speed = 7
        self.jump_speed = -14
        self.jump_true = True # Stop a lot of jumping in the game
        self.gravity = 0.6
        self.wait_for_release = True  # Prevent movement until keys are released

    def get_input(self):  # Handles keyboard input for movement and jumping
        keys = pygame.key.get_pressed()  # Get the current state of all keys

        # Wait until all movement/jump keys are released
        if self.wait_for_release:
            keys = pygame.key.get_pressed()
            if not any([keys[pygame.K_RIGHT], keys[pygame.K_d],
                        keys[pygame.K_LEFT], keys[pygame.K_a],
                        keys[pygame.K_UP], keys[pygame.K_w],
                        keys[pygame.K_SPACE]]):
                self.wait_for_release = False  # All keys released
            else:
                self.direction.x = 0
                return  # Skip movement input until release

        # Horizontal movement (Right) When right arrow and D key is press 
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.image = self.maui_right_run
            self.facing_right = True 

        # Horizontal movement (Left) When left arrow and A key is press
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.image = self.maui_left_run
            self.facing_right = False

        else:  # No horizontal movement. When no key is press.
            self.direction.x = 0
           # Idle animation based on last direction
            if self.image in [self.maui_right_run, self.maui_right_idle]:
                self.image = self.maui_right_idle
            else:
                self.image = self.maui_left_idle

        # Jumping When Up, Space Bar and W key press.
        if self.jump_true:
            if keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]: 
                self.jump()  # Apply upward force
                self.jump_true = False  # Prevent double jumping


    # Gravitly so the Maui does not flyalway
    def apply_gravity(self): # Have gravity to the character
            self.direction.y += self.gravity
            self.rect.y += self.direction.y
    def jump(self):
            self.direction.y = self.jump_speed  # Negative value to move upward

    def animate(self):
        if self.direction.x != 0: # Choose animation frames based on movement direction
            frames = self.maui_right_run if self.facing_right else self.maui_left_run  # If moving horizontally, use running animation
        else:
            frames = self.maui_right_idle if self.facing_right else self.maui_left_idle # If standing still, use idle animation
        self.frame_index += self.animation_speed
        if self.frame_index >= len(frames): # Loop back to the start if user reached the end of the frame list
            self.frame_index = 0
        self.image = frames[int(self.frame_index)] # Set the current image to the appropriate frame

    def update(self): # Find player input
        self.get_input()
        self.animate()

