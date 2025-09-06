# Joshua Lee
# 2025/07/15
# Version 1.2 - Added adjustable player hitbox

import pygame
from pygame.locals import *

# Initialize pygame
pygame.init()

# Set up the game clock and frames per second
clock = pygame.time.Clock()
fps = 60

# Set up the screen dimensions
screen_width = 800
screen_height = 600

# Create the game window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')

# Define game variables
main_menu = True  # Flag to track if we're in the main menu
tile_size = 50    # Size of each tile in pixels
game_over = 0     # 0 = playing, 1 = level complete, -1 = game over
player_width = 40 # Width of player hitbox
player_height = 80  # Height of player hitbox
enemy_width = 45   # Width of enemy hitbox
enemy_height = 45  # Height of enemy hitbox
score = 0         # Player's score (coins collected)
level = 1         # Current level
max_levels = 3    # Maximum number of levels
col_thresh = 10   # Collision threshold for platforms

# Define colours
white = (255, 255, 255)
blue = (0, 0, 255)

# Define fonts
font = pygame.font.SysFont('Arial', 70)      # Large font for game messages
font_score = pygame.font.SysFont('Arial', 30) # Smaller font for score display

# Load images
sun_img = pygame.image.load('img/sun.png')        # Sun decoration for background
bg_img = pygame.image.load('img/forest_sky.png')         # Background sky image
restart_img = pygame.image.load('img/restart_btn.png')  # Restart button image
start_img = pygame.image.load('img/start_btn.png')      # Start button image
exit_img = pygame.image.load('img/exit_btn.png')        # Exit button image

# Load sounds
pygame.mixer.music.load('sound/music.wav')  # Background music
pygame.mixer.music.play(-1, 0.0, 5000)     # Play music on loop
coin_fx = pygame.mixer.Sound('sound/coin.wav')      # Coin collection sound
coin_fx.set_volume(0.5)                            # Set volume to 50%
jump_fx = pygame.mixer.Sound('sound/jump.wav')      # Jump sound
jump_fx.set_volume(0.5)                            # Set volume to 50%
game_over_fx = pygame.mixer.Sound('sound/game_over.wav')  # Game over sound
game_over_fx.set_volume(0.5)                           # Set volume to 50%

def draw_text(text, font, text_col, x, y):
    
    #Draw text on the screen at the specified position.

    img = font.render(text, True, text_col)  # Render the text as an image
    screen.blit(img, (x, y))                 # Draw the text image on screen

def reset_level(level):
   
    # Select the appropriate level data based on the level number
    if level == 1:
        data = world_data
    elif level == 2:
        data = level2_data
    elif level == 3:
        data = level3_data
        
    # Find the spawn point in the level data
    spawn_x, spawn_y = find_spawn_point(data)
    # Reset the player to the spawn point
    player.reset(spawn_x, spawn_y)
    # Clear all sprite groups
    taniwha_group.empty()
    platform_group.empty()
    coin_group.empty()
    lava_group.empty()
    exit_group.empty()
    # Return a new World object with the level data
    return World(data)  

def find_spawn_point(data):
    
    #Find the player spawn point in the level data.
    
    
    # Iterate through the level data to find the spawn point (tile value 9)
    for y, row in enumerate(data):
        for x, tile in enumerate(row):
            if tile == 9:
                # Return the coordinates multiplied by tile size
                return x * tile_size, y * tile_size
    # Default spawn point if none is found
    return 100, screen_height - 130

class Button():
    #A class to create interactive buttons.
    
    def __init__(self, x, y, image):
        
        #Initialize a button.
        
        
        self.image = image                    # Button image
        self.rect = self.image.get_rect()     # Rectangle for collision detection
        self.rect.x = x                       # Set x position
        self.rect.y = y                       # Set y position
        self.clicked = False                  # Track if button is clicked

    def draw(self):
        
        #Draw the button and check for clicks.
    
        action = False  # Initialize action to False
        pos = pygame.mouse.get_pos()  # Get mouse position
        
        # Check if mouse is over button
        if self.rect.collidepoint(pos):
            # Check if left mouse button is pressed and button wasn't already clicked
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True          # Set action to True
                self.clicked = True    # Mark button as clicked
        
        # Reset clicked state when mouse button is released
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
            
        # Draw the button on screen
        screen.blit(self.image, self.rect)
        return action  # Return whether button was clicked

class Player():
    #A class to represent the player character.
    
    def __init__(self, x, y):
        #Initialize the player at the specified position.
        self.reset(x, y)  # Call reset to set up the player

    def update(self, game_over):
        
        #Update the player's position and state.

        dx = 0  # Change in x position
        dy = 0  # Change in y position
        walk_cooldown = 5  # Controls animation speed

        # Only process input if game is not over
        if game_over == 0:
            # Get keyboard input
            key = pygame.key.get_pressed()
            
            # Jump if space or W is pressed, player is on ground, and not already jumping
            if (key[pygame.K_SPACE] or key[pygame.K_w]) and self.jumped == False and self.in_air == False:
                self.vel_y = -15  # Set upward velocity
                self.jumped = True  # Mark as jumped
                jump_fx.play()     # Play jump sound
                
            # Reset jump state when space/W is released
            if key[pygame.K_SPACE] == False:
                self.jumped = False
                
            # Move left if left arrow or A is pressed
            if key[pygame.K_LEFT] or key[pygame.K_a]:
                dx -= 5           # Move left
                self.counter += 1 # Increment animation counter
                self.direction = -1  # Set direction to left
                
            # Move right if right arrow or D is pressed
            if key[pygame.K_RIGHT] or key[pygame.K_d]:
                dx += 5           # Move right
                self.counter += 1 # Increment animation counter
                self.direction = 1   # Set direction to right
                
            # Reset animation if no movement keys are pressed
            if (key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False and 
                key[pygame.K_a] == False and key[pygame.K_d] == False):
                self.counter = 0  # Reset animation counter
                self.index = 0    # Reset animation frame index
                
            # Handle animation
            if self.counter > walk_cooldown:
                self.counter = 0    # Reset counter
                self.index += 1     # Move to next animation frame
                # Loop back to first frame if at end
                if self.index >= len(self.images_right):
                    self.index = 0
                # Set image based on direction
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # Apply gravity
            self.vel_y += 1
            # Terminal velocity
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y  # Add vertical velocity to movement

        # Assume player is in air until proven otherwise
        self.in_air = True

        # Update hitbox position to match player position
        self.hitbox.x = self.rect.x + self.hitbox_offset_x
        self.hitbox.y = self.rect.y + self.hitbox_offset_y

        # Check for collision with tiles
        for tile in world.tile_list:
            # Check for horizontal collision
            if tile[1].colliderect(self.hitbox.x + dx, self.hitbox.y, self.hitbox_width, self.hitbox_height):
                dx = 0  # Stop horizontal movement
            # Check for vertical collision
            if tile[1].colliderect(self.hitbox.x, self.hitbox.y + dy, self.hitbox_width, self.hitbox_height):
                # If moving upward (jumping)
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.hitbox.top  # Adjust position
                    self.vel_y = 0  # Stop upward movement
                # If moving downward (falling)
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.hitbox.bottom  # Adjust position
                    self.vel_y = 0  # Stop downward movement
                    self.in_air = False  # Player is on ground

        # Check for collision with moving platforms
        for platform in platform_group:
            # Check for horizontal collision with platforms
            if platform.rect.colliderect(self.hitbox.x + dx, self.hitbox.y, self.hitbox_width, self.hitbox_height):
                dx = 0  # Stop horizontal movement
            # Check for vertical collision with platforms
            if platform.rect.colliderect(self.hitbox.x, self.hitbox.y + dy, self.hitbox_width, self.hitbox_height):
                # If landing on top of platform
                if abs((self.hitbox.bottom + dy) - platform.rect.top) < col_thresh:
                    self.hitbox.bottom = platform.rect.top  # Position player on platform
                    self.in_air = False  # Player is on platform
                    dy = 0  # Stop vertical movement
                # If platform moves horizontally, move player with it
                elif platform.move_x != 0:
                    self.rect.x += platform.move_direction

        # Apply movement to player's main rect
        self.rect.x += dx
        self.rect.y += dy
        
        # Update hitbox position after movement
        self.hitbox.x = self.rect.x + self.hitbox_offset_x
        self.hitbox.y = self.rect.y + self.hitbox_offset_y

        # Check for collision with enemies
        for taniwha in taniwha_group:
            if self.hitbox.colliderect(taniwha.get_hitbox()):
                game_over = -1  # Game over if hit enemy
                game_over_fx.play()  # Play game over sound
                break

        # Check for collision with lava
        for lava in lava_group:
            if self.hitbox.colliderect(lava.rect):
                game_over = -1  # Game over if touched lava
                game_over_fx.play()  # Play game over sound
                break

        # Check for collision with exit
        for exit in exit_group:
            if self.hitbox.colliderect(exit.rect):
                game_over = 1  # Level complete if reached exit
                break

        # Handle game over state
        if game_over == -1:
            self.image = self.dead_image  # Change to dead image
            # Make player float upward
            if self.rect.y > 200:
                self.rect.y -= 5

        # Draw the player on screen (adjusted for camera scroll)
        screen.blit(self.image, (self.rect.x - scroll[0], self.rect.y - scroll[1]))
        
        # Debug: Draw hitbox (visible for debugging collision)
        pygame.draw.rect(screen, (255, 0, 0), (self.hitbox.x - scroll[0], self.hitbox.y - scroll[1], self.hitbox_width, self.hitbox_height), 2)
        
        return game_over  # Return updated game state

    def reset(self, x, y):
        
        #Reset the player to initial state at the specified position.
        
        self.images_right = []  # List of right-facing animation frames
        self.images_left = []   # List of left-facing animation frames
        self.index = 0          # Current animation frame index
        self.counter = 0        # Animation counter
        
        # Load and scale player animation frames
        for num in range(1, 5):
            img_right = pygame.image.load(f'img/guy{num}.png')
            # Calculate aspect ratio to maintain proportions
            original_width, original_height = img_right.get_size()
            aspect_ratio = original_width / original_height
            new_height = player_height
            new_width = int(aspect_ratio * new_height)
            # Scale image to desired size
            img_right = pygame.transform.scale(img_right, (new_width, new_height))
            # Create left-facing version by flipping image
            img_left = pygame.transform.flip(img_right, True, False)
            # Add images to lists
            self.images_right.append(img_right)
            self.images_left.append(img_left)
            
        # Load and scale dead player image
        self.dead_image = pygame.image.load('img/wairua.png')
        original_width, original_height = self.dead_image.get_size()
        aspect_ratio = original_width / original_height
        new_height = player_height
        new_width = int(aspect_ratio * new_height)
        self.dead_image = pygame.transform.scale(self.dead_image, (new_width, new_height))
    
        # Set current image and position
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
        # Define hitbox properties (smaller than the visual representation)
        self.hitbox_width = player_width - 10   # Hitbox width
        self.hitbox_height = player_height - 13 # Hitbox height
        # Calculate offset to center hitbox
        self.hitbox_offset_x = (self.width - self.hitbox_width) // 2
        self.hitbox_offset_y = self.height - self.hitbox_height
        
        # Create hitbox rectangle
        self.hitbox = pygame.Rect(
            self.rect.x + self.hitbox_offset_x,
            self.rect.y + self.hitbox_offset_y,
            self.hitbox_width,
            self.hitbox_height
        )
        
        # Initialize movement properties
        self.vel_y = 0      # Vertical velocity
        self.jumped = False # Jump state
        self.direction = 0  # Facing direction
        self.in_air = True  # Airborne state

class World():
    #A class to represent the game world and handle tile rendering."""
    
    def __init__(self, data):
        
        #Initialize the world from level data.
        
        
        self.tile_list = []  # List to store all tiles
        
        # Load tile images
        dirt_img = pygame.image.load('img/dirt.png')
        grass_img = pygame.image.load('img/grass.png')
        
        row_count = 0
        # Process each row in the level data
        for row in data:
            col_count = 0
            # Process each tile in the row
            for tile in row:
                # Dirt tile (1)
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                # Grass tile (2)
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                # Enemy (3)
                if tile == 3:
                    taniwha = Enemy(col_count * tile_size, row_count * tile_size)
                    taniwha_group.add(taniwha)
                # Horizontal moving platform (4)
                if tile == 4:
                    platform = Platform(col_count * tile_size, row_count * tile_size, 1, 0)
                    platform_group.add(platform)
                # Vertical moving platform (5)
                if tile == 5:
                    platform = Platform(col_count * tile_size, row_count * tile_size, 0, 1)
                    platform_group.add(platform)
                # Lava (6)
                if tile == 6:
                    lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    lava_group.add(lava)
                # Coin (7)
                if tile == 7:
                    coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    coin_group.add(coin)
                # Exit (8)
                if tile == 8:
                    exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))
                    exit_group.add(exit)
                col_count += 1  # Move to next column
            row_count += 1  # Move to next row

    def draw(self):
        """Draw all tiles in the world (adjusted for camera scroll)."""
        for tile in self.tile_list:
            screen.blit(tile[0], (tile[1].x - scroll[0], tile[1].y - scroll[1]))

class Enemy(pygame.sprite.Sprite):
    #A class to represent enemy characters.
    
    def __init__(self, x, y):
        
        #Initialize an enemy at the specified position.
        
        pygame.sprite.Sprite.__init__(self)
        # Load and scale enemy image
        self.image = pygame.image.load('img/shadow_taniwha.png')
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Define hitbox properties (smaller than visual representation)
        self.hitbox_width = tile_size - 30 
        self.hitbox_height = tile_size - 10 
        self.hitbox_offset_x = 5  # Horizontal offset to center hitbox
        self.hitbox_offset_y = 5  # Vertical offset to center hitbox
        
        # Movement properties
        self.move_direction = 1    # Direction of movement (1 = right, -1 = left)
        self.move_counter = 0      # Counter to track movement

    def update(self):
        #Update enemy position (patrol back and forth).

        self.rect.x += self.move_direction  # Move enemy
        self.move_counter += 1              # Increment movement counter
        # Reverse direction after moving 50 pixels
        if abs(self.move_counter) > 50:
            self.move_direction *= -1  # Reverse direction
            self.move_counter *= -1    # Reset counter

    def get_hitbox(self):
        
        #Get the enemy's hitbox rectangle.
        
        return pygame.Rect(
            self.rect.x + self.hitbox_offset_x,
            self.rect.y + self.hitbox_offset_y,
            self.hitbox_width,
            self.hitbox_height
        )

class Platform(pygame.sprite.Sprite):
    #A class to represent moving platforms.
    
    def __init__(self, x, y, move_x, move_y):
        
        #Initialize a platform.
        
        pygame.sprite.Sprite.__init__(self)
        # Load and scale platform image
        img = pygame.image.load('img/platform.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # Movement properties
        self.move_counter = 0      # Counter to track movement
        self.move_direction = 1    # Direction of movement
        self.move_x = move_x       # Horizontal movement flag
        self.move_y = move_y       # Vertical movement flag

    def update(self):
        #Update platform position.

        # Move platform based on direction and movement flags
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1  # Increment movement counter
        # Reverse direction after moving 50 pixels
        if abs(self.move_counter) > 50:
            self.move_direction *= -1  # Reverse direction
            self.move_counter *= -1    # Reset counter

class Coin(pygame.sprite.Sprite):
    #A class to represent collectible coins.
    
    def __init__(self, x, y):
        
        #Initialize a coin at the specified position.
        
        pygame.sprite.Sprite.__init__(self)
        # Load and scale coin image
        img = pygame.image.load('img/coin.png')
        self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # Center the coin

class Exit(pygame.sprite.Sprite):
    #A class to represent the level exit.
    
    def __init__(self, x, y):
        
        #Initialize an exit at the specified position.
       
        pygame.sprite.Sprite.__init__(self)
        # Load and scale exit image
        img = pygame.image.load('img/exit.png')
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Lava(pygame.sprite.Sprite):
    #A class to represent lethal lava.
    
    def __init__(self, x, y):
        
        #Initialize lava at the specified position.
        
        pygame.sprite.Sprite.__init__(self)
        # Load and scale lava image
        img = pygame.image.load('img/lava.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# World data for level 1 - Basic platformer level
# 0 = empty, 1 = dirt, 2 = grass, 3 = enemy, 4 = horizontal platform, 
# 5 = vertical platform, 6 = lava, 7 = coin, 8 = exit, 9 = player spawn
world_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1], 
[1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 2, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 2, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1], 
[1, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1], 
[1, 0, 2, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 2, 2, 2, 2, 1], 
[1, 0, 0, 0, 0, 0, 2, 2, 2, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 9, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# World data for level 2 - Mountain theme
level2_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 7, 0, 0, 8, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 2, 1], 
[1, 0, 0, 0, 0, 7, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 2, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 2, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 2, 2, 2, 6, 2, 6, 2, 2, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 1, 1, 1, 1, 1, 1, 1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 7, 7, 0, 0, 0, 7, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 1], 
[1, 9, 0, 2, 6, 6, 6, 2, 2, 2, 2, 1, 1, 6, 6, 6, 6, 6, 6, 1], 
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# World data for level 3 - Underground cave theme
level3_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 7, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 8, 1], 
[1, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 2, 0, 2, 2, 1], 
[1, 0, 0, 0, 0, 2, 6, 2, 6, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 1], 
[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 1], 
[1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 1], 
[1, 6, 6, 6, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 2, 7, 7, 7, 1], 
[1, 1, 1, 1, 1, 1, 1, 0, 2, 2, 2, 0, 0, 0, 0, 1, 2, 7, 7, 1], 
[1, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 0, 1, 1, 2, 7, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 1, 1, 1, 2, 1], 
[1, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 9, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Find initial spawn point from level 1 data
spawn_x, spawn_y = find_spawn_point(world_data)
# Create player at spawn point
player = Player(spawn_x, spawn_y)

# Create sprite groups for different game objects
taniwha_group = pygame.sprite.Group()        # Enemy group
platform_group = pygame.sprite.Group()    # Moving platforms group
lava_group = pygame.sprite.Group()        # Lava group
coin_group = pygame.sprite.Group()        # coins group
exit_group = pygame.sprite.Group()        # Level exit group

# Create a coin for displaying score (top left corner)
score_coin = Coin(tile_size // 2, tile_size // 2)
coin_group.add(score_coin)

# Create the initial world from level 1 data
world = World(world_data)

# Create UI buttons
restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 100, restart_img)
start_button = Button(screen_width // 2 - 350, screen_height // 2, start_img)
exit_button = Button(screen_width // 2 + 150, screen_height // 2, exit_img)

# Camera scroll offset
scroll = [0, 0]

# Main game loop
run = True
while run:
    clock.tick(fps)  # Maintain consistent frame rate
    
    # Draw background
    screen.blit(bg_img, (0, 0))
    screen.blit(sun_img, (100, 100))

    # Handle main menu state
    if main_menu:
        # Draw exit button and check for click
        if exit_button.draw():
            run = False  # Quit game if exit button clicked
        # Draw start button and check for click
        if start_button.draw():
            main_menu = False  # Exit main menu
            # Initialize camera scroll to center on player
            scroll[0] = player.rect.x - screen_width // 2
            scroll[1] = player.rect.y - screen_height // 2
    else:
        # Gameplay state
        
        # Calculate target camera position to follow player
        target_x = player.rect.x - screen_width // 2
        target_y = player.rect.y - screen_height // 2
        # Smoothly interpolate camera position
        scroll[0] += (target_x - scroll[0]) // 10
        scroll[1] += (target_y - scroll[1]) // 10
        # Clamp camera to level boundaries
        scroll[0] = max(0, min(scroll[0], len(world_data[0]) * tile_size - screen_width))
        scroll[1] = max(0, min(scroll[1], len(world_data) * tile_size - screen_height))
        
        # Draw the world
        world.draw()

        # Update game objects if game is not over
        if game_over == 0:
            taniwha_group.update()        # Update enemies
            platform_group.update()    # Update moving platforms
            # Check for coin collection
            if pygame.sprite.spritecollide(player, coin_group, True):
                score += 1        # Increment score
                coin_fx.play()    # Play coin sound
            # Draw score counter
            draw_text('X ' + str(score), font_score, white, tile_size - 10, 10)
        
        # Draw all game objects (adjusted for camera scroll)
        for taniwha in taniwha_group:
            screen.blit(taniwha.image, (taniwha.rect.x - scroll[0], taniwha.rect.y - scroll[1]))
        for platform in platform_group:
            screen.blit(platform.image, (platform.rect.x - scroll[0], platform.rect.y - scroll[1]))
        for lava in lava_group:
            screen.blit(lava.image, (lava.rect.x - scroll[0], lava.rect.y - scroll[1]))
        for coin in coin_group:
            screen.blit(coin.image, (coin.rect.x - scroll[0], coin.rect.y - scroll[1]))
        for exit in exit_group:
            screen.blit(exit.image, (exit.rect.x - scroll[0], exit.rect.y - scroll[1]))

        # Update player and get game state
        game_over = player.update(game_over)

        # Handle game over state (player died)
        if game_over == -1:
            # Draw restart button and check for click
            if restart_button.draw():
                # Reset level
                world = reset_level(level)
                game_over = 0      # Reset game state
                score = 0          # Reset score
                # Reset camera scroll
                scroll = [player.rect.x - screen_width // 2, player.rect.y - screen_height // 2]

        # Handle level completion
        if game_over == 1:
            level += 1  # Advance to next level
            # Check if there are more levels
            if level <= max_levels:
                # Reset to next level
                world = reset_level(level)
                game_over = 0  # Reset game state
                # Reset camera scroll
                scroll = [player.rect.x - screen_width // 2, player.rect.y - screen_height // 2]
            else:
                # Player has completed all levels
                draw_text('YOU WIN!', font, blue, (screen_width // 2) - 140, screen_height // 2)
                # Draw restart button and check for click
                if restart_button.draw():
                    level = 1  # Reset to level 1
                    world = reset_level(level)
                    game_over = 0  # Reset game state
                    score = 0      # Reset score
                    # Reset camera scroll
                    scroll = [player.rect.x - screen_width // 2, player.rect.y - screen_height // 2]

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Window close event
            run = False  # End game loop

    # Update display
    pygame.display.update()

# Clean up pygame
pygame.quit()