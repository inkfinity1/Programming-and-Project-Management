# GAME VERSION 1.2
# AUTHOR: Derek WU
# Date: 2025/07/28
# main_asset.py

import pygame
import sys

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Load and scale the background image and information button
def load_assets():
    try:
        background_img = pygame.image.load("graphics/maori_art_main.png").convert_alpha()
        background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

        information_button_img = pygame.image.load("graphics/information_button.png").convert_alpha()
        information_button_img = pygame.transform.scale(information_button_img, (160, 40))

        info_image = pygame.image.load("graphics/information_page.png").convert_alpha()
        info_image = pygame.transform.scale(info_image, (WIDTH, HEIGHT))

        game_one= pygame.image.load("graphics/game_one.jpg").convert_alpha()
        game_one = pygame.transform.scale(game_one, (100, 50))

        return background_img, information_button_img, info_image, game_one
    except pygame.error:
        print("Error: Could not load an image.")
        sys.exit()

