# Ngā Taonga o Māui (The Treasures of Māui)
# GAME VERSION 1.2
# AUTHOR: Derek WU
# Date: 2025/07/28

import pygame
import sys
from main_asset import load_assets
from sound_asset import load_sounds



# Init
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ngā Taonga o Māui")

# Load assets
background_img, information_button_img, info_image, game_one = load_assets()
click_sound = load_sounds()

# Rects
information_button_rect = information_button_img.get_rect(topleft=(0, 0))
game_button_rect = game_one.get_rect(topleft=(60, 60))

# State
in_main_menu = True

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif in_main_menu and event.type == pygame.MOUSEBUTTONDOWN:
            if information_button_rect.collidepoint(event.pos):
                if click_sound:
                    click_sound.play()

                screen.blit(info_image, (0, 0))
                pygame.display.update()

                info_screen = True
                while info_screen:
                    for info_event in pygame.event.get():
                        if info_event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif info_event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                            info_screen = False
                            if click_sound:
                                click_sound.play()

            elif game_button_rect.collidepoint(event.pos):
                if click_sound:
                    click_sound.play()
                in_main_menu = False  # Leave the menu and go into the game

    if in_main_menu:
        screen.blit(background_img, (0, 0))
        screen.blit(information_button_img, information_button_rect)
        screen.blit(game_one, game_button_rect)
        pygame.display.update()


pygame.quit()
sys.exit()
