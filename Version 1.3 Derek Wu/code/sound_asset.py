
# GAME VERSION 1.3
# AUTHOR: Derek WU
# Date: 2025/08/04

import pygame

def load_sounds(): # Function to load sound effects used in the game
    pygame.mixer.init() # Initialize the Pygame mixer module 

    try:
        click_sound = pygame.mixer.Sound("sound/click_fx.wav") # Load the click sound effect from the 'sound' folder
        return click_sound
    except pygame.error:
        print("Error: Could not load sound.")
        return None  # Return None so the game can continue running without crashing
