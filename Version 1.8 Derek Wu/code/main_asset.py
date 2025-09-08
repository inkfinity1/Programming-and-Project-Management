# Ngā Taonga o Māui (The Treasures of Māui)
#GAME VERSION 1.8
# AUTHOR: Derek WU
# Date: 2025/09/08
# Main asset

import pygame
import sys

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Image for the main page.
# Load and scale some of the image and button
def load_assets():
    try:
        # Level background
        background_level_one = pygame.image.load("graphics/alevel_one_background.jpg").convert_alpha()
        background_level_one = pygame.transform.scale( background_level_one, (WIDTH, HEIGHT))

        background_level_two = pygame.image.load("graphics/alevel_two_background.jpg").convert_alpha()
        background_level_two = pygame.transform.scale( background_level_two, (WIDTH, HEIGHT))

        background_level_three = pygame.image.load("graphics/alevel_three_background.jpg").convert_alpha()
        background_level_three = pygame.transform.scale( background_level_three, (WIDTH, HEIGHT))

        background_level_four = pygame.image.load("graphics/alevel_four_background.png").convert_alpha()
        background_level_four = pygame.transform.scale( background_level_four, (WIDTH, HEIGHT))
        
        background_img = pygame.image.load("graphics/maori_art_main.png").convert_alpha()
        background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

        information_button_img = pygame.image.load("graphics/ainformation_button.png").convert_alpha()
        information_button_img = pygame.transform.scale(information_button_img, (225, 50))

        info_img = pygame.image.load("graphics/ainformation_page.png").convert_alpha()
        info_img = pygame.transform.scale(info_img, (WIDTH, HEIGHT))

        game_button = pygame.image.load("graphics/play.png").convert_alpha()
        game_button = pygame.transform.scale(game_button, (300, 300))

        instruction_button = pygame.image.load("graphics/ainstruction.jpg").convert_alpha()
        instruction_button = pygame.transform.scale(instruction_button, (300, 40))

        home_button = pygame.image.load("graphics/home.png").convert_alpha()
        home_button = pygame.transform.scale(home_button, (100,100))
        
        exit_button = pygame.image.load("graphics/exit_button.png").convert_alpha()
        exit_button  = pygame.transform.scale(exit_button, (100,100))

        instruction_page = pygame.image.load("graphics/ainstruction_page.jpg").convert_alpha()
        instruction_page  = pygame.transform.scale( instruction_page , (WIDTH, HEIGHT))

        objective_page = pygame.image.load("graphics/objective.jpg").convert_alpha()
        objective_page= pygame.transform.scale(objective_page, (WIDTH, HEIGHT))


        return (background_img, information_button_img, info_img, game_button, background_level_one, 
        background_level_two, background_level_three, background_level_four, instruction_button, home_button, 
        exit_button, instruction_page, objective_page)
    except pygame.error:
        print("Error: Could not load an main assets.")
        sys.exit()


def load_block_assets():
    try:
        #Load tiles images
        # Load and scale
        grass_block_img = pygame.image.load('graphics/grass_block.png').convert_alpha()
        grass_block_img = pygame.transform.scale(grass_block_img, (100, 72))

        dirt_block_img = pygame.image.load('graphics/dirt_block.png').convert_alpha()
        dirt_block_img = pygame.transform.scale(dirt_block_img, (100, 72))

        kiwi_block_img = pygame.image.load('graphics/kiwi.png').convert_alpha()
        kiwi_block_img = pygame.transform.scale(kiwi_block_img, (100, 60))

        lava_block_img = pygame.image.load('graphics/alava_block.png').convert_alpha()
        lava_block_img = pygame.transform.scale(lava_block_img, (100, 70))

        return  grass_block_img, dirt_block_img, kiwi_block_img, lava_block_img
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

        maui_left_idle = pygame.image.load("graphics/maui_idle_left.png").convert_alpha()
        maui_left_idle = pygame.transform.scale(maui_left_idle, (54, 100))

        return maui_right_run, maui_left_run, maui_right_idle, maui_left_idle

    except pygame.error:
        print("Error: Could not load character images.")
        sys.exit()
