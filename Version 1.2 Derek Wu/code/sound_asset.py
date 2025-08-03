# GAME VERSION 1.2
# AUTHOR: Derek WU
# Date: 2025/07/28

import pygame


def load_sounds():
    pygame.mixer.init()
    try:
        click_sound = pygame.mixer.Sound("sound/click_fx.wav")
        return click_sound
    except pygame.error:
        print("Error: Could not load sound.")
        return None