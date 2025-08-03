# GAME VERSION 1.2
# AUTHOR: Derek WU
# Date: 2025/07/28
import pygame
from block import Tile

class Player(pygame.sprite.Sprite):


    def __init__(self, pos): #pos gets pass in through level which is where the player gets drawn in
        super().__init__()
        
        #Imports palyer graphics
        self.maui_right_run = pygame.transform.scale(pygame.image.load('graphics/maui_run_right.png'),(48,96)).convert_alpha()
        self.maui_left_run = pygame.transform.scale(pygame.image.load('graphics/maui_run_left.png'),(48,96)).convert_alpha()
        self.maui_left_idle = pygame.transform.scale(pygame.image.load('graphics/maui_idle_left.png'),(48,96)).convert_alpha()
        self.maui_right_idle = pygame.transform.scale(pygame.image.load('graphics/maui_idle_right.png'),(48,96)).convert_alpha()
        self.player_state = self.maui_right_idle
        self.image = self.player_state
        #self.image = pygame.transform.scale(pygame.image.load('graphics/maui_idle_right.png'),(48,96)).convert_alpha()
        #self.image = pygame.Surface((32,64))
        #self.image.fill('red')
        self.rect= self.image.get_rect(topleft = pos)
        
        #Player Movement
        self.direction = pygame.math.Vector2(0,0) #Vector stores x and y values in a list
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16
        self.jump_true = True #Prevents infinite jumps



    def get_input (self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.image = self.maui_right_run
            

        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.image = self.maui_left_run

        else:
            self.direction.x = 0

        if self.jump_true:
            if keys[pygame.K_UP]: 
                self.jump()
                self.jump_true = False

    def apply_gravity(self):
        self.direction.y += self.gravity #increase the speed of gravity every frame to make it more realistic
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed #Makes the player jump by changing its y value (Constant)

    def update(self):
        self.get_input()
       
