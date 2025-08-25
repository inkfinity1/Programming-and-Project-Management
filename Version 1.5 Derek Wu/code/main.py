# Ngā Taonga o Māui (The Treasures of Māui)
# GAME VERSION 1.5
# AUTHOR: Derek WU
# Date: 2025/08/18

# Set up
import pygame
import sys
from main_asset import load_assets
from sound_asset import load_sounds
from settings_for_levels import Level
from map import level_map_1, level_map_2, level_map_3

# Init
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ngā Taonga o Māui")
clock = pygame.time.Clock()

# Load assets
(background_img, information_button_img, info_img, game_button, background_level_one,
 background_level_two, background_level_three, instruction_button, home_button) = load_assets()

click_sound = load_sounds()

# Rects
information_button_rect = information_button_img.get_rect(topleft=(0, 0))
game_button_rect = game_button.get_rect(topleft=(250, 200))
instruction_button_rect = instruction_button.get_rect(topleft=(250, 500))
home_button_rect = home_button.get_rect(topleft=(10, HEIGHT - home_button.get_height() - 10))

# Game state
in_main_menu = True
current_level_index = 0
levels = [level_map_1, level_map_2, level_map_3]
backgrounds = [background_level_one, background_level_two, background_level_three]
level = Level(levels[current_level_index], screen)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Main menu interactions
        elif in_main_menu and event.type == pygame.MOUSEBUTTONDOWN: # Information page
            if information_button_rect.collidepoint(event.pos):
                if click_sound:
                    click_sound.play()

                screen.blit(info_img, (0, 0))
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

            elif instruction_button_rect.collidepoint(event.pos): # Instruction page
                if click_sound:
                    click_sound.play()

                screen.blit(background_level_one, (0, 0)) # still need to make instruction image, waiting for joshua to help me 
                pygame.display.update()

                instruction_screen = True
                while instruction_screen:
                    for instruction_event in pygame.event.get():
                        if instruction_event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif instruction_event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                            instruction_screen = False
                            if click_sound:
                                click_sound.play()

            elif game_button_rect.collidepoint(event.pos): # Game page
                if click_sound:
                    click_sound.play()
                in_main_menu = False  # Start the game

        # In-game interactions
        elif not in_main_menu and event.type == pygame.MOUSEBUTTONDOWN: # Home/Menu page
            if home_button_rect.collidepoint(event.pos):
                if click_sound:
                    click_sound.play()
                in_main_menu = True  # Return to main menu

    # Rendering
    if in_main_menu:
        screen.blit(background_img, (0, 0))
        screen.blit(information_button_img, information_button_rect)
        screen.blit(game_button, game_button_rect)
        screen.blit(instruction_button, instruction_button_rect)
    else:
        screen.blit(backgrounds[current_level_index], (0, 0))
        screen.blit(home_button, home_button_rect)  

        if level.run():  # If player reaches transition tile
            current_level_index += 1
            if current_level_index < len(levels):
                level = Level(levels[current_level_index], screen)
            else:
                print("🎉 All levels completed!")
                in_main_menu = True
                current_level_index = 0
                level = Level(levels[current_level_index], screen)

    pygame.display.update()
    clock.tick(60)

# Exit
pygame.quit()
sys.exit()

