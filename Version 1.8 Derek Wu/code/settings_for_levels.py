# Ngā Taonga o Māui (The Treasures of Māui)
#GAME VERSION 1.8
# AUTHOR: Derek WU
# Date: 2025/09/08
# Setting for levels
import pygame
from map import Tile, tile_size, screen_width
from maui import Player
from sound_asset import effects

male_kiwi = effects()

class Level: 
    def __init__(self, level_data, surface):
        # Store reference to display surface (the game screen)
        self.display_surface = surface
        # Store level data and create the layout
        self.level_data = level_data
        self.setup_level(level_data)
        # Level progression state
        self.next_level = False
        # Scrolling and world movement
        self.world_shift = 0
        self.scroll = True
        # Default scroll position limit
        self._posX = screen_width - (screen_width / 2)
        # Player respawn state
        self.respawn = True

    def setup_level(self,layout):
        self.player = pygame.sprite.GroupSingle()
        self.tiles = pygame.sprite.Group()
        self.unsafe_tile = pygame.sprite.Group()
        self.lava_tile = pygame.sprite.Group()
        self.trans_tiles = pygame.sprite.Group()

        for row_index, row in enumerate(layout):  # Loop through each row in the level layout with its index
            for column_index, cell in enumerate(row): # Loop through each cell in the row with its column index
                
                # Calculate pixel position for each tile (60x60 spacing)
                x = column_index * tile_size  
                y = row_index * tile_size  
            
                if cell == 'P':             # Place Maui to the spawn point on the map.
                    player_sprite = Player((x,y))
                    self.player.add(player_sprite)

                if cell == 'G':             # Place a grass block/tile
                    tile = Tile((x,y),'grass')
                    self.tiles.add(tile)

                if cell == 'D':             # Place a drit block/tile
                    tile = Tile((x,y),'dirt')
                    self.tiles.add(tile)
                
                if cell == 'K':            # Place a kiwi 
                    unsafe_tile = Tile((x, y), 'kiwi')
                    self.unsafe_tile.add(unsafe_tile)

                if cell == 'L':            ## Place a lava block/tile
                    lava_tile = Tile((x,y), 'lava')
                    self.lava_tile.add(lava_tile)

                if cell == 'N':             # Place a transparent grass block/tile on move to the next level.
                    trans_tile = Tile((x,y), 'grass')
                    self.trans_tiles.add(trans_tile)
            
    def handle_horizontal_collisions(self):
        player = self.player.sprite

        # Move horizontally
        player.rect.x += player.direction.x * player.speed

        # Check collision with solid tiles
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:  # Moving left
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:  # Moving right
                    player.rect.right = sprite.rect.left

    def handle_vertical_collisions(self):
        player = self.player.sprite

        # Apply gravity
        player.direction.y += player.gravity
        player.rect.y += player.direction.y

        # Check collision with solid tiles
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:  # Falling
                    player.rect.bottom = sprite.rect.top
                    player.jump_true = True
                    player.direction.y = 0
                elif player.direction.y < 0:  # Jumping
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0

    def scroll_w(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        # # Enable scrolling when allowed
        if self.scroll: # Scroll world to the right if player moves left near the left edge
            if player_x < screen_width / 2 and direction_x < 0:
                self.world_shift = 6
                player.speed = 0
            elif player_x > self._posX and direction_x > 0: # Scroll world to the left if player moves right near the right edge
                self.world_shift = -6
                player.speed = 0
            else: # No scroll needed; allow normal movement
                self.world_shift = 0
                player.speed = 6
        else:
            # Stop scrolling 
            self.world_shift = 0
            player.speed = 6
            # Re-enable scroll if maui moves far enough left
            if player_x < 600:
                self.world_shift = 6
                self.scroll = True

    def check_fall_out_map(self): 
        player = self.player.sprite
        # If maui falls below screen boundary, trigger respawn
        if player.rect.y > 600:
            self.respawn = True
        if self.respawn: # Reset level if maui is marked dead
            self.setup_level(self.level_data) # Reload level layout 
            self.respawn = False

    def check_lava_collision(self): # lava collision 
        player = self.player.sprite
        for tile in self.lava_tile.sprites(): 
            if tile.rect.colliderect(player.rect): # If the user touches lava it respawn the Maui
                self.respawn = True
              
    def check_unsafe_collision(self): # Kiwi collison 
        player = self.player.sprite
        for tile in self.unsafe_tile.sprites(): 
            if tile.rect.colliderect(player.rect): # If the user touches Kiwi it respawn the Maui
                self.respawn = True

                if male_kiwi:
                 for _ in range(5): # Dramatic echo effect to increase the volume to make it higher than the game music
                    male_kiwi.play()
                    self.kiwi_start_time = pygame.time.get_ticks()  # record start time
            # Stop kiwi sound after 5 seconds
        if hasattr(self, 'kiwi_start_time'):
            if pygame.time.get_ticks() - self.kiwi_start_time > 1000:
                male_kiwi.stop()
                del self.kiwi_start_time  # clean up

        if self.respawn:
            self.setup_level(self.level_data)
            self.respawn = False

    def check_collistion_with_next_tile(self):
        player = self.player.sprite  # Access the player sprite from the group

        # Loop through all transition tiles (marked 'N' in the map)
        for sprite_ in self.trans_tiles.sprites():
            # Check collision between maui and transition tiles 
            if sprite_.rect.colliderect(player.rect):
                # If maui touched a transition tile, mark the level as complete
                self.next_level = True

    def run(self):
        # Update and draw level tiles (grass, dirt)
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)

         # Update and draw transition tiles (used for level completion)
        self.trans_tiles.update(self.world_shift)
        self.trans_tiles.draw(self.display_surface)

        self.scroll_w() # Handle horizontal scrolling logic

        # Update and draw unsafe tiles and lava tiles (used for danger zones)
        self.unsafe_tile.update(self.world_shift)
        self.unsafe_tile.draw(self.display_surface)
        self.lava_tile.update(self.world_shift)
        self.lava_tile.draw(self.display_surface)

        # Update maui movement and handle collisions
        self.player.update()  # handles input
        self.handle_horizontal_collisions()  # move left/right and resolve collisions
        self.handle_vertical_collisions()    # apply gravity and resolve vertical collisions

        self.player.draw(self.display_surface)

        # Check if maui has fallen off the map or touches a unsafe tile
        self.check_fall_out_map()
        self.check_unsafe_collision()
        self.check_lava_collision()

        # Check if maui has reached a transition tile ('N') 
        self.check_collistion_with_next_tile() 
        # Return whether to progress to the next level
        return self.next_level

