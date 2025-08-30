
# Ngā Taonga o Māui (The Treasures of Māui)
# GAME VERSION 1.6
# AUTHOR: Derek WU
# Date: 2025/08/25
# Sound assets

import pygame

def load_sounds(): # Function to load sound effects used in the game
    pygame.mixer.init() # Initialize the Pygame mixer module 

    try:
        click_sound = pygame.mixer.Sound("sound/click_fx.wav") # Load the click sound effect from the 'sound' folder
        return click_sound
    except pygame.error:
        print("Error: Could not load sound.")
        return None  # Return None so the game can continue running without crashing
        

def effects(): # Function to load sound effects used in the game
    pygame.mixer.init() # Initialize the Pygame mixer module 

    try:
        male_kiwi = pygame.mixer.Sound("sound/male_kiwi.wav") # Load the click sound effect from the 'sound' folder
        return male_kiwi
    except pygame.error:
        print("Error: Could not load sound.")
        return None  # Return None so the game can continue running without crashing