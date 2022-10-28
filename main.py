from curses import window
from tkinter import CENTER
from turtle import window_height
import pygame
import pygame
import neat
import time
import os
import random
import tkinter

#Set the dimensions of the game screen
WIN_WIDTH = 600
WIN_HEIGHT = 800

#Load in image assets to pygame.
FLOPPY_BIRDS_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
FLOOR_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "floor.png")))
BACKGROUND_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "background.png")))

#Sprite class - Floppy Bird
class Floppy_Bird:
    SPRITES = FLOPPY_BIRDS_IMGS
    #Define sprite movement constraints
    MAX_ROTATION = 25
    ROTATION_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        #Starting position of sprite.
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.sprite_count = 0
        self.sprite = self.SPRITES[0]
        
    #Method: Move sprite up.
    def jump(self):
        #Set negative velocity to move bird up on the grid.
        self.vel = -10.5

        self.tick_count = 0
        self.height = self.y

    #Method: Call every frame to move bird 'forward'.
    def move(self):
        #Track movement with every frame tick.
        self.tick_count += 1

        #Calculate displacement. i.e How many pixels to move up or down per frame.
        displacement = self.vel*self.tick_count + 1.5*self.tick_count**2

        #Set terminal velocity to prevent sprite from moving too far up or down.
        if displacement >= 16:
            displacement = 16

        if displacement < 0:
            displacement -= 2

        #Change sprite position based on displacement.
        self.y = self.y + displacement

        #Determine if sprite is tilting up or down and action on it.
        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROTATION_VEL

    #Draw sprite current position to window.
    def draw(self, win):
        #Track times that main game loop has run.
        self.sprite_count += 1

        #Check which sprite to show based on tick count.
        if self.sprite_count < self.ANIMATION_TIME:
            self.sprite = self.SPRITES[0]
        elif self.sprite_count < self.ANIMATION_TIME*2:
            self.sprite = self.SPRITES[1]
        elif self.sprite_count < self.ANIMATION_TIME*3:
            self.sprite = self.SPRITES[2]
        elif self.sprite_count < self.ANIMATION_TIME*4:
            self.sprite = self.SPRITES[1]
        elif self.sprite_count == self.ANIMATION_TIME*4 + 1:
            self.sprite = self.SPRITES[0]
            self.sprite_count = 0

        #If sprite is falling straight down show neutral sprite instead of movement sprites.
        if self.tilt <= -80:
            self.sprite = self.SPRITES[1]
            self.sprite_count = self.ANIMATION_TIME*2

        #Rotate image around its center. Don't really know how this works. Copied.
        rotated_sprite = pygame.transform.rotate(self.sprite, self.tilt)
        new_rectangle = rotated_sprite.get_rect(center=self.sprite.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_sprite, new_rectangle.topleft)
    
    #Colision detection.
    def get_mask(self):
        return pygame.mask.from_surface(self.sprite)


#Function to draw to window.
def draw_window(win, sprite):
    win.blit(BACKGROUND_IMG, (0,0))
    sprite.draw(win)

    pygame.display.update()

#Main game loop.
def main():
    sprite = Floppy_Bird(200,200)
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    #Begin Main game loop
    run_game = True
    while run_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False

        draw_window(win, sprite)        
    pygame.quit()
    quit()

main()




