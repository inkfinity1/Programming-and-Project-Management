# Ngā Taonga o Māui (The Treasures of Māui)
# GAME VERSION 1.1
# AUTHOR: Derek WU
# Date: 2025/07/20

import pygame
import sys
from main_asset import load_assets 
from sound_asset import load_sounds
# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ngā Taonga o Māui")

# Load assets
background_img, information_button_img, info_image = load_assets()

# Load sound assets
click_sound = load_sounds()



# Button positioning
information_button_rect = information_button_img.get_rect()
information_button_rect.topleft = (0,0)

# Main game loop
running = True
while running:
    screen.blit(background_img, (0, 0))
    screen.blit(information_button_img, information_button_rect)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if information_button_rect.collidepoint(event.pos):
                if click_sound:
                         click_sound.play()

                screen.blit(info_image, (0,0))
                pygame.display.update()
 
                    # Temporary information screen
                info_screen = True
                while info_screen:
                    for info_event in pygame.event.get():
                        if info_event.type == pygame.QUIT:
                             pygame.quit()
                             sys.exit()
                        elif info_event.type == pygame.KEYDOWN or info_event.type == pygame.MOUSEBUTTONDOWN:
                                info_screen = False
                                click_sound.play()
                

# Exit
pygame.quit()
sys.exit()


