import pygame
from pygame.locals import *

class PlatformerGame:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        
        # Set up the game clock and frames per second
        self.clock = pygame.time.Clock()
        self.fps = 60
        
        # Set up the screen dimensions
        self.screen_width = 800
        self.screen_height = 600
        
        # Create the game window
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Platformer')
        
        # Define game variables
        self.main_menu = False  # Changed to False to start game immediately
        self.tile_size = 50
        self.game_over = 0
        self.player_width = 40
        self.player_height = 80
        self.enemy_width = 45
        self.enemy_height = 45
        self.score = 0
        self.level = 1
        self.max_levels = 3
        self.col_thresh = 10
        
        # Define colours
        self.white = (255, 255, 255)
        self.blue = (0, 0, 255)
        
        # Define fonts
        self.font = pygame.font.SysFont('Arial', 70)
        self.font_score = pygame.font.SysFont('Arial', 30)
        
        # Load images
        self.sun_img = pygame.image.load('img/sun.png')
        self.bg_img = pygame.image.load('img/forest_sky.png')
        self.restart_img = pygame.image.load('img/restart_btn.png')
        
        # Load sounds
        pygame.mixer.music.load('sound/music.wav')
        pygame.mixer.music.play(-1, 0.0, 5000)
        self.coin_fx = pygame.mixer.Sound('sound/coin.wav')
        self.coin_fx.set_volume(0.5)
        self.jump_fx = pygame.mixer.Sound('sound/jump.wav')
        self.jump_fx.set_volume(0.5)
        self.game_over_fx = pygame.mixer.Sound('sound/game_over.wav')
        self.game_over_fx.set_volume(0.5)
        
        # World data for levels
        self.world_data = [
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
        
        self.level2_data = [
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
        
        self.level3_data = [
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
        spawn_x, spawn_y = self.find_spawn_point(self.world_data)
        # Create player at spawn point
        self.player = self.Player(self, spawn_x, spawn_y)
        
        # Create sprite groups for different game objects
        self.taniwha_group = pygame.sprite.Group()
        self.platform_group = pygame.sprite.Group()
        self.lava_group = pygame.sprite.Group()
        self.coin_group = pygame.sprite.Group()
        self.exit_group = pygame.sprite.Group()
        
        # Create a coin for displaying score (top left corner)
        score_coin = self.Coin(self, self.tile_size // 2, self.tile_size // 2)
        self.coin_group.add(score_coin)
        
        # Create the initial world from level 1 data
        self.world = self.World(self, self.world_data)
        
        # Create restart button only (no start or exit buttons)
        self.restart_button = self.Button(self, self.screen_width // 2 - 50, self.screen_height // 2 + 100, self.restart_img)
        
        # Initialize camera scroll to center on player
        self.scroll = [self.player.rect.x - self.screen_width // 2, self.player.rect.y - self.screen_height // 2]
        
        # Game running state
        self.running = True

    def draw_text(self, text, font, text_col, x, y):
        #Draw text on the screen at the specified position.
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))

    def reset_level(self, level):
        #Reset the level with the appropriate level data.
        # Select the appropriate level data based on the level number
        if level == 1:
            data = self.world_data
        elif level == 2:
            data = self.level2_data
        elif level == 3:
            data = self.level3_data
        
        # Find the spawn point in the level data
        spawn_x, spawn_y = self.find_spawn_point(data)
        # Reset the player to the spawn point
        self.player.reset(spawn_x, spawn_y)
        # Clear all sprite groups
        self.taniwha_group.empty()
        self.platform_group.empty()
        self.coin_group.empty()
        self.lava_group.empty()
        self.exit_group.empty()
        # Return a new World object with the level data
        return self.World(self, data)  

    def find_spawn_point(self, data):
        #Find the player spawn point in the level data.
        # Iterate through the level data to find the spawn point (tile value 9)
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile == 9:
                    # Return the coordinates multiplied by tile size
                    return x * self.tile_size, y * self.tile_size
        # Default spawn point if none is found
        return 100, self.screen_height - 130

    def run(self):
        #Main game loop.
        while self.running:
            self.clock.tick(self.fps)
            
            # Draw background
            self.screen.blit(self.bg_img, (0, 0))
            self.screen.blit(self.sun_img, (100, 100))

            # Game starts immediately - no main menu
            
            # Calculate target camera position to follow player
            target_x = self.player.rect.x - self.screen_width // 2
            target_y = self.player.rect.y - self.screen_height // 2
            # Smoothly interpolate camera position
            self.scroll[0] += (target_x - self.scroll[0]) // 10
            self.scroll[1] += (target_y - self.scroll[1]) // 10
            # Clamp camera to level boundaries
            self.scroll[0] = max(0, min(self.scroll[0], len(self.world_data[0]) * self.tile_size - self.screen_width))
            self.scroll[1] = max(0, min(self.scroll[1], len(self.world_data) * self.tile_size - self.screen_height))
            
            # Draw the world
            self.world.draw()

            # Update game objects if game is not over
            if self.game_over == 0:
                self.taniwha_group.update()
                self.platform_group.update()
                # Check for coin collection
                if pygame.sprite.spritecollide(self.player, self.coin_group, True):
                    self.score += 1
                    self.coin_fx.play()
                # Draw score counter
                self.draw_text('X ' + str(self.score), self.font_score, self.white, self.tile_size - 10, 10)
            
            # Draw all game objects (adjusted for camera scroll)
            for taniwha in self.taniwha_group:
                self.screen.blit(taniwha.image, (taniwha.rect.x - self.scroll[0], taniwha.rect.y - self.scroll[1]))
            for platform in self.platform_group:
                self.screen.blit(platform.image, (platform.rect.x - self.scroll[0], platform.rect.y - self.scroll[1]))
            for lava in self.lava_group:
                self.screen.blit(lava.image, (lava.rect.x - self.scroll[0], lava.rect.y - self.scroll[1]))
            for coin in self.coin_group:
                self.screen.blit(coin.image, (coin.rect.x - self.scroll[0], coin.rect.y - self.scroll[1]))
            for exit in self.exit_group:
                self.screen.blit(exit.image, (exit.rect.x - self.scroll[0], exit.rect.y - self.scroll[1]))

            # Update player and get game state
            self.game_over = self.player.update(self.game_over)

            # Handle game over state (player died)
            if self.game_over == -1:
                # Draw restart button and check for click
                if self.restart_button.draw():
                    # Reset level
                    self.world = self.reset_level(self.level)
                    self.game_over = 0
                    self.score = 0
                    # Reset camera scroll
                    self.scroll = [self.player.rect.x - self.screen_width // 2, self.player.rect.y - self.screen_height // 2]

            # Handle level completion
            if self.game_over == 1:
                self.level += 1
                # Check if there are more levels
                if self.level <= self.max_levels:
                    # Reset to next level
                    self.world = self.reset_level(self.level)
                    self.game_over = 0
                    # Reset camera scroll
                    self.scroll = [self.player.rect.x - self.screen_width // 2, self.player.rect.y - self.screen_height // 2]
                else:
                    #add a win screen here
                    # Player has completed all levels
                    self.draw_text('YOU WIN!', self.font, self.blue, (self.screen_width // 2) - 140, self.screen_height // 2)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Update display
            pygame.display.update()

    class Button:
        def __init__(self, game, x, y, image):
            self.game = game
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.clicked = False

        def draw(self):
            action = False
            pos = pygame.mouse.get_pos()
        
            # Check if mouse is over button
            if self.rect.collidepoint(pos):
                # Check if left mouse button is pressed and button wasn't already clicked
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    action = True
                    self.clicked = True
        
            # Reset clicked state when mouse button is released
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
            
            # Draw the button on screen
            self.game.screen.blit(self.image, self.rect)
            return action

    class Player:
        def __init__(self, game, x, y):
            self.game = game
            self.reset(x, y)

        def update(self, game_over):
            dx = 0
            dy = 0
            walk_cooldown = 5

            # Only process input if game is not over
            if game_over == 0:
                # Get keyboard input
                key = pygame.key.get_pressed()
            
                # Jump if space or W is pressed, player is on ground, and not already jumping
                if (key[pygame.K_SPACE] or key[pygame.K_w] or key[pygame.K_UP]) and self.jumped == False and self.in_air == False:
                    self.vel_y = -15
                    self.jumped = True
                    self.game.jump_fx.play()
                
                # Reset jump state when space/W is released
                if key[pygame.K_SPACE] == False:
                    self.jumped = False
                
                # Move left if left arrow or A is pressed
                if key[pygame.K_LEFT] or key[pygame.K_a]:
                    dx -= 5
                    self.counter += 1
                    self.direction = -1
                
                # Move right if right arrow or D is pressed
                if key[pygame.K_RIGHT] or key[pygame.K_d]:
                    dx += 5
                    self.counter += 1
                    self.direction = 1
                
                # Reset animation if no movement keys are pressed
                if (key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False and 
                    key[pygame.K_a] == False and key[pygame.K_d] == False):
                    self.counter = 0
                    self.index = 0
                
                # Handle animation
                if self.counter > walk_cooldown:
                    self.counter = 0
                    self.index += 1
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
                dy += self.vel_y

            # Assume player is in air
            self.in_air = True

            # Update hitbox position to match player position
            self.hitbox.x = self.rect.x + self.hitbox_offset_x
            self.hitbox.y = self.rect.y + self.hitbox_offset_y

            # Check for collision with tiles
            for tile in self.game.world.tile_list:
                # Check for horizontal collision
                if tile[1].colliderect(self.hitbox.x + dx, self.hitbox.y, self.hitbox_width, self.hitbox_height):
                    dx = 0
                # Check for vertical collision
                if tile[1].colliderect(self.hitbox.x, self.hitbox.y + dy, self.hitbox_width, self.hitbox_height):
                    # If moving upward (jumping)
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.hitbox.top
                        self.vel_y = 0
                    # If moving downward (falling)
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.hitbox.bottom
                        self.vel_y = 0
                        self.in_air = False

            # Check for collision with moving platforms
            for platform in self.game.platform_group:
                # Check for horizontal collision with platforms
                if platform.rect.colliderect(self.hitbox.x + dx, self.hitbox.y, self.hitbox_width, self.hitbox_height):
                    dx = 0
                # Check for vertical collision with platforms
                if platform.rect.colliderect(self.hitbox.x, self.hitbox.y + dy, self.hitbox_width, self.hitbox_height):
                    # If landing on top of platform
                    if abs((self.hitbox.bottom + dy) - platform.rect.top) < self.game.col_thresh:
                        self.hitbox.bottom = platform.rect.top
                        self.in_air = False
                        dy = 0
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
            for taniwha in self.game.taniwha_group:
                if self.hitbox.colliderect(taniwha.get_hitbox()):
                    game_over = -1
                    self.game.game_over_fx.play()
                    break

            # Check for collision with lava
            for lava in self.game.lava_group:
                if self.hitbox.colliderect(lava.rect):
                    game_over = -1
                    self.game.game_over_fx.play()
                    break

            # Check for collision with exit
            for exit in self.game.exit_group:
                if self.hitbox.colliderect(exit.rect):
                    game_over = 1
                    break

            # Handle game over state
            if game_over == -1:
                self.image = self.dead_image
                # Make player float upward
                if self.rect.y > 200:
                    self.rect.y -= 5

            # Draw the player on screen (adjusted for camera scroll)
            self.game.screen.blit(self.image, (self.rect.x - self.game.scroll[0], self.rect.y - self.game.scroll[1]))
        
            return game_over

        def reset(self, x, y):
            self.images_right = []
            self.images_left = []
            self.index = 0
            self.counter = 0
        
            # Load and scale player animation frames
            for num in range(1, 5):
                img_right = pygame.image.load(f'img/guy{num}.png')
                # Calculate aspect ratio to maintain proportions
                original_width, original_height = img_right.get_size()
                aspect_ratio = original_width / original_height
                new_height = self.game.player_height
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
            new_height = self.game.player_height
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
            self.hitbox_width = self.game.player_width - 10
            self.hitbox_height = self.game.player_height - 13
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
            self.vel_y = 0
            self.jumped = False
            self.direction = 0
            self.in_air = True

    class World:
        def __init__(self, game, data):
            self.game = game
            self.tile_list = []
        
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
                        img = pygame.transform.scale(dirt_img, (self.game.tile_size, self.game.tile_size))
                        img_rect = img.get_rect()
                        img_rect.x = col_count * self.game.tile_size
                        img_rect.y = row_count * self.game.tile_size
                        tile = (img, img_rect)
                        self.tile_list.append(tile)
                    # Grass tile (2)
                    if tile == 2:
                        img = pygame.transform.scale(grass_img, (self.game.tile_size, self.game.tile_size))
                        img_rect = img.get_rect()
                        img_rect.x = col_count * self.game.tile_size
                        img_rect.y = row_count * self.game.tile_size
                        tile = (img, img_rect)
                        self.tile_list.append(tile)
                    # Enemy (3)
                    if tile == 3:
                        taniwha = self.game.Enemy(self.game, col_count * self.game.tile_size, row_count * self.game.tile_size)
                        self.game.taniwha_group.add(taniwha)
                    # Horizontal moving platform (4)
                    if tile == 4:
                        platform = self.game.Platform(self.game, col_count * self.game.tile_size, row_count * self.game.tile_size, 1, 0)
                        self.game.platform_group.add(platform)
                    # Vertical moving platform (5)
                    if tile == 5:
                        platform = self.game.Platform(self.game, col_count * self.game.tile_size, row_count * self.game.tile_size, 0, 1)
                        self.game.platform_group.add(platform)
                    # Lava (6)
                    if tile == 6:
                        lava = self.game.Lava(self.game, col_count * self.game.tile_size, row_count * self.game.tile_size + (self.game.tile_size // 2))
                        self.game.lava_group.add(lava)
                    # Coin (7)
                    if tile == 7:
                        coin = self.game.Coin(self.game, col_count * self.game.tile_size + (self.game.tile_size // 2), row_count * self.game.tile_size + (self.game.tile_size // 2))
                        self.game.coin_group.add(coin)
                    # Exit (8)
                    if tile == 8:
                        exit = self.game.Exit(self.game, col_count * self.game.tile_size, row_count * self.game.tile_size - (self.game.tile_size // 2))
                        self.game.exit_group.add(exit)
                    col_count += 1
                row_count += 1

        def draw(self):
            for tile in self.tile_list:
                self.game.screen.blit(tile[0], (tile[1].x - self.game.scroll[0], tile[1].y - self.game.scroll[1]))

    class Enemy(pygame.sprite.Sprite):
        def __init__(self, game, x, y):
            self.game = game
            pygame.sprite.Sprite.__init__(self)
            # Load and scale enemy image
            self.image = pygame.image.load('img/shadow_taniwha.png')
            self.image = pygame.transform.scale(self.image, (self.game.tile_size, self.game.tile_size))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
        
            # Define hitbox properties (smaller than visual representation)
            self.hitbox_width = self.game.tile_size - 30 
            self.hitbox_height = self.game.tile_size - 10 
            self.hitbox_offset_x = 5
            self.hitbox_offset_y = 5
        
            # Movement properties
            self.move_direction = 1
            self.move_counter = 0

        def update(self):
            self.rect.x += self.move_direction
            self.move_counter += 1
            # Reverse direction after moving 50 pixels
            if abs(self.move_counter) > 50:
                self.move_direction *= -1
                self.move_counter *= -1

        def get_hitbox(self):
            return pygame.Rect(
                self.rect.x + self.hitbox_offset_x,
                self.rect.y + self.hitbox_offset_y,
                self.hitbox_width,
                self.hitbox_height
            )

    class Platform(pygame.sprite.Sprite):
        def __init__(self, game, x, y, move_x, move_y):
            self.game = game
            pygame.sprite.Sprite.__init__(self)
            # Load and scale platform image
            img = pygame.image.load('img/platform.png')
            self.image = pygame.transform.scale(img, (self.game.tile_size, self.game.tile_size // 2))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            # Movement properties
            self.move_counter = 0
            self.move_direction = 1
            self.move_x = move_x
            self.move_y = move_y

        def update(self):
            # Move platform based on direction and movement flags
            self.rect.x += self.move_direction * self.move_x
            self.rect.y += self.move_direction * self.move_y
            self.move_counter += 1
            # Reverse direction after moving 50 pixels
            if abs(self.move_counter) > 50:
                self.move_direction *= -1
                self.move_counter *= -1

    class Coin(pygame.sprite.Sprite):
        def __init__(self, game, x, y):
            self.game = game
            pygame.sprite.Sprite.__init__(self)
            # Load and scale coin image
            img = pygame.image.load('img/coin.png')
            self.image = pygame.transform.scale(img, (self.game.tile_size // 2, self.game.tile_size // 2))
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)

    class Exit(pygame.sprite.Sprite):
        def __init__(self, game, x, y):
            self.game = game
            pygame.sprite.Sprite.__init__(self)
            # Load and scale exit image
            img = pygame.image.load('img/exit.png')
            self.image = pygame.transform.scale(img, (self.game.tile_size, int(self.game.tile_size * 1.5)))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

    class Lava(pygame.sprite.Sprite):
        def __init__(self, game, x, y):
            self.game = game
            pygame.sprite.Sprite.__init__(self)
            # Load and scale lava image
            img = pygame.image.load('img/lava.png')
            self.image = pygame.transform.scale(img, (self.game.tile_size, self.game.tile_size // 2))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

# To run this game standalone
if __name__ == "__main__":
    game = PlatformerGame()
    game.run()
    pygame.quit()