# GAME VERSION 1.4
# AUTHOR: Derek WU
# Date: 2025/08/11
# main_asset.py

import pygame
import sys

# Screen dimensions
WIDTH, HEIGHT = 800, 600


# Image for the main page.
# Load and scale the image and button
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

        background_level_one = pygame.image.load("graphics/level_1_background.jpg").convert_alpha()
        background_level_one = pygame.transform.scale( background_level_one, (WIDTH, HEIGHT))

        background_level_two = pygame.image.load("graphics/level_2_background.jpg").convert_alpha()
        background_level_two = pygame.transform.scale( background_level_two, (WIDTH, HEIGHT))

        background_level_three = pygame.image.load("graphics/level_3_background.jpg").convert_alpha()
        background_level_three = pygame.transform.scale( background_level_three, (WIDTH, HEIGHT))

        return background_img, information_button_img, info_image, game_one, background_level_one, background_level_two,background_level_three
    except pygame.error:
        print("Error: Could not load an main assets.")
        sys.exit()


def load_block_assets():
    try:
        #Load tiles images
        grass_block_img =  pygame.image.load('graphics/grass_block.png').convert_alpha()
        dirt_block_img = pygame.image.load('graphics/dirt_block.png').convert_alpha()

        return  grass_block_img, dirt_block_img 
    except pygame.error:
        print("Error: Could not load block images.")
        sys.exit()


def load_character_assets():
    try:
        # Character graphics 
        # Load and scale
        maui_right_run = pygame.image.load("graphics/maui_run_right.png").convert_alpha()
        maui_right_run = pygame.transform.scale(maui_right_run, (65, 100))

        maui_left_run = pygame.image.load("graphics/maui_run_left.png").convert_alpha()
        maui_left_run = pygame.transform.scale(maui_left_run, (65, 100))

        maui_right_idle = pygame.image.load("graphics/maui_idle_right.png").convert_alpha()
        maui_right_idle = pygame.transform.scale(maui_right_idle, (54, 100))

        return maui_right_run, maui_left_run, maui_right_idle

    except pygame.error:
        print("Error: Could not load character images.")
        sys.exit()
