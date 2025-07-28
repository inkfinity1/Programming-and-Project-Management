# GAME VERSION 1.1
# AUTHOR: Derek WU
# Date: 2025/07/20

import pygame
import sys

def load_sounds():
    pygame.mixer.init()
    try:
        click_sound = pygame.mixer.Sound("sound/click_fx.wav")
        return click_sound
    except pygame.error:
        print("Error: Could not load sound.")
        return None