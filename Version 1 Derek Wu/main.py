# Ngā Taonga o Māui (The Treasures of Māui)
# GAME VERSION 1.1
# AUTHOR: Derek WU
# Date: 2025/07/17

import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ngā Taonga o Māui")

# Load and scale the background image and information button image
try:
    background_img = pygame.image.load("maori_art_main.png").convert()
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
    information_button_img = pygame.image.load("information_button.png").convert_alpha()
    information_button_img = pygame.transform.scale(information_button_img, (80, 60))
except pygame.error:
    print("Error: Could not load an image.")
    sys.exit()

# Click sound When button is press
pygame.mixer.init()
try:
    click_sound = pygame.mixer.Sound("click_fx.wav")  
except pygame.error:
    print("Error: Could not load sound.")
    click_sound = None

# Get button rect and position
information_button_rect = information_button_img.get_rect()
information_button_rect.topleft = (0,0)

# Font and color
font = pygame.font.SysFont('Arial', 40)
WHITE = (255, 255, 255)

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
                try:
                    info_image = pygame.image.load("backgrounddefault.jpg").convert()
                    info_image = pygame.transform.scale(info_image, (WIDTH, HEIGHT))
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
                except pygame.error:
                    print("Error: Could not load the info image.")

# Exit
pygame.quit()
sys.exit()

