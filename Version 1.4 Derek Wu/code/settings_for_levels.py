# GAME VERSION 1.4
# AUTHOR: Derek WU
# Date: 2025/08/11
import pygame
from map import Tile, tile_size, screen_width
from player import Player

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

        # Player respawn state
        self.dead = True

        # Default scroll position limit
        self._posX = screen_width - (screen_width / 2)

    def setup_level(self,layout):
        self.tiles = pygame.sprite.Group()
        self.trans_tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        for row_index, row in enumerate(layout):  # Loop through each row in the level layout with its index
            for col_index, cell in enumerate(row): # Loop through each cell in the row with its column index
                
                # Calculate pixel position for each tile (60x60 spacing)
                x = col_index * tile_size  
                y = row_index * tile_size  

                if cell == 'G':             # Place a grass block/tile
                    tile = Tile((x,y),'grass')
                    self.tiles.add(tile)

                if cell == 'D':             # Place a drit block/tile
                    tile = Tile((x,y),'dirt')
                    self.tiles.add(tile)

                if cell == 'P':             # Place Maui to the spawn point on the map.
                    player_sprite = Player((x,y))
                    self.player.add(player_sprite)

                if cell == 'T':             # Place a transparent grass block/tile on move to the next level.
                    trans_tile = Tile((x,y), 'grass')
                    self.trans_tiles.add(trans_tile)                

    def pass_level(self):
        player = self.player.sprite  # Access the player sprite from the group

        # Loop through all transition tiles (marked 'T' in the map)
        for sprite_ in self.trans_tiles.sprites():
            # Check collision between maui and transition tiles 
            if sprite_.rect.colliderect(player.rect):
                # If maui touched a transition tile, mark the level as complete
                self.next_level = True

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        # # Enable scrolling when allowed
        if self.scroll: # Scroll world to the right if player moves left near the left edge
            if player_x < screen_width / 2 and direction_x < 0:
                self.world_shift = 8
                player.speed = 0
            elif player_x > self._posX and direction_x > 0: # Scroll world to the left if player moves right near the right edge
                self.world_shift = -8
                player.speed = 0
            else: # No scroll needed; allow normal movement
                self.world_shift = 0
                player.speed = 8
        else:
            # Stop scrolling 
            self.world_shift = 0
            player.speed = 8
            # Re-enable scroll if maui moves far enough left
            if player_x < 600:
                self.world_shift = 8
                self.scroll = True

    def vertical_movement_collisions(self):
            player = self.player.sprite
            player.apply_gravity()  
            # Check collision with solid tiles (grass, dirt) so maui doesn't fall through or jumping through tiles
            for sprite in self.tiles.sprites():
                if sprite.rect.colliderect(player.rect):
                    if player.direction.y > 0: # Collision while falling down
                        player.rect.bottom = sprite.rect.top
                        player.jump_true = True
                        player.direction.y = 0
                    elif player.direction.y < 0: # Collision while jumping up
                        player.rect.top = sprite.rect.bottom 
                        player.direction.y = 0

    def horizontal_movement_collisions(self):
        player = self.player.sprite
         # Move player horizontally based on direction and speed
        player.rect.x += player.direction.x * player.speed
        # Check collision with solid tiles (grass, dirt)
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left

    def check_fall_out_map(self):
        player = self.player.sprite
        # If maui falls below screen boundary, trigger respawn
        if player.rect.y > 715:
            self.dead = True
        if self.dead: # Reset level if maui is marked dead
            self.setup_level(self.level_data) # Reload level layout 
            self.dead = False



    def run(self):
        # Update and draw level tiles (grass, dirt)
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)

         # Update and draw transition tiles (used for level completion)
        self.trans_tiles.update(self.world_shift)
        self.trans_tiles.draw(self.display_surface)

        self.pass_level() # Check if maui has reached a transition tile ('T')
        self.scroll_x() # Handle horizontal scrolling logic

         # Update maui movement and handle collisions
        self.player.update()
        self.horizontal_movement_collisions()
        self.vertical_movement_collisions()
        self.player.draw(self.display_surface)

        # Check if maui has fallen off the map
        self.check_fall_out_map()
 
        # Return whether to progress to the next level
        return self.next_level

