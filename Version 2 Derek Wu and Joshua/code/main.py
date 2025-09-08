# Ngā Taonga o Māui (The Treasures of Māui)
# GAME VERSION 2 Combining games Joshau Lee's and Derek Wu
# AUTHOR: Derek WU
# Date: 2025/09/08

# Set up
import pygame
import sys
from main_asset import load_assets
from sound_asset import load_sounds
from settings_for_levels import Level
from map import level_map_1, level_map_2, level_map_3, level_map_4
from maui_hunting import PlatformerGame

# Init
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ngā Taonga o Māui")
clock = pygame.time.Clock()

# Load assets
(background_img, information_button_img, info_img, game_button, background_level_one,
 background_level_two, background_level_three, background_level_four, instruction_button, home_button, exit_button, 
 instruction_page, objective,joushua_page) = load_assets()
#load sound assets
click_sound = load_sounds()
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1, fade_ms= 1000)  # Loop foverevr and 1 second fade-in each time

# Rects and location
information_button_rect = information_button_img.get_rect(topleft=(0, 0))
game_button_rect = game_button.get_rect(topleft=(250, 200))
instruction_button_rect = instruction_button.get_rect(topleft=(250, 500))
home_button_rect = home_button.get_rect(topleft=(10, HEIGHT - home_button.get_height() - 10))
exit_button_rect = exit_button.get_rect(bottomright=(WIDTH - 10, HEIGHT - 10))

# Game state
in_main_menu = True
current_level_index = 0
levels = [level_map_1, level_map_2, level_map_3, level_map_4]
backgrounds = [background_level_one, background_level_two, background_level_three,background_level_four]
level = Level(levels[current_level_index], screen)

# Sound and display image 
def show_static_page(image, click_sound):
    screen.blit(image, (0, 0)) # Load image on screen with location (0,0)
    pygame.display.update() # Update the display so the image appears
    page_open = True
    while page_open:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN): # See if mouse or key press exit the page
                page_open = False # If its false it exit the page
                if click_sound:
                    click_sound.play() # Play a sound when exiting the page

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif in_main_menu and event.type == pygame.MOUSEBUTTONDOWN:
            if information_button_rect.collidepoint(event.pos): # Imformation button
                if click_sound: # plays click sound
                    click_sound.play()
                show_static_page(info_img, click_sound) # Opens imformation page with click sound

            elif instruction_button_rect.collidepoint(event.pos): # Instruction button
                if click_sound: 
                    click_sound.play() # plays click sound
                show_static_page(instruction_page, click_sound) # Opens instruction page with click sound

            elif game_button_rect.collidepoint(event.pos): # Game button
                if click_sound:
                    click_sound.play() # plays click sound
                show_static_page(objective, click_sound) # Opens objective/storyline of game with click sound
                show_static_page(instruction_page, click_sound) # Opens instruction page with click sound
                in_main_menu = False # Opens my game

            elif exit_button_rect.collidepoint(event.pos): # Right side exit button 
                if click_sound:
                    click_sound.play() # plays click sound
                    pygame.time.delay(300) # Pause/delay the game for 300 milliseconds
                running = False # Exit the Termail

        elif not in_main_menu and event.type == pygame.MOUSEBUTTONDOWN: 
            if home_button_rect.collidepoint(event.pos): # Home button
                if click_sound:
                    click_sound.play() # plays click sound
                in_main_menu = True # Go back to main/home page save game

            elif exit_button_rect.collidepoint(event.pos):  # Right side exit button
                if click_sound:
                    click_sound.play() # plays click sound
                    pygame.time.delay(300) # Pause/delay the game for 300 milliseconds
                running = False # Exit the Termail

    # Rendering/ load the grahics.
    if in_main_menu:
        screen.blit(background_img, (0, 0))
        screen.blit(information_button_img, information_button_rect)
        screen.blit(game_button, game_button_rect)
        screen.blit(instruction_button, instruction_button_rect)
        screen.blit(exit_button, exit_button_rect)
    else:
        screen.blit(backgrounds[current_level_index], (0, 0))
        screen.blit(home_button, home_button_rect)
        screen.blit(exit_button, exit_button_rect)

        # Check if the current level is completed    
        if level.run():
            current_level_index += 1
            if current_level_index < len(levels):
                level = Level(levels[current_level_index], screen)
            else:
                # Runs Joshua Lee game
                show_static_page(joushua_page, click_sound) # Opens ones my game is completed Joshua Lee instruction page with click sound
                game_instance = PlatformerGame(screen) # Start Joshua's game using the current screen
                game_instance.run() # Runs Joshua Lee game

                print("All levels completed. Well done!") # Print on Termail
                in_main_menu = True # Go back to main/home page
                current_level_index = 0
                level = Level(levels[current_level_index], screen)

    pygame.display.update()
    clock.tick(60)

# Exit
pygame.quit()
sys.exit()

