from turtle import width
import pygame
import neat
import time
import os
import random
import tkinter
pygame.font.init()

#Set the dimensions of the game screen
WIN_WIDTH = 500
WIN_HEIGHT = 800

#Load in image assets to pygame.
FLOPPY_BIRDS_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
OBSTACLE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
FLOOR_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "floor.png")))
BACKGROUND_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "background.png")))
SCORE_FONT = pygame.font.SysFont("Verdana", 25)

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
    
    #Collision detection.
    def get_mask(self):
        return pygame.mask.from_surface(self.sprite)

class Obstacle:
    GAP = 200
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        
        self.top = 0
        self.bottom = 0
        self.OBSTACLE_TOP = pygame.transform.flip(OBSTACLE_IMG, False, True)
        self.OBSTACLE_BOTTOM = OBSTACLE_IMG

        self.passed = False

        self.set_height()

    #Define obstacle height randomly for variation.
    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.OBSTACLE_TOP.get_height()
        self.bottom = self.height + self.GAP

    #Move obstacle to the left.
    def move(self):
        self.x -= self.VEL

    #Draw Obstacle.
    def draw(self, win):
        win.blit(self.OBSTACLE_TOP, (self.x, self.top))
        win.blit(self.OBSTACLE_BOTTOM, (self.x, self.bottom))

    #Collision detections using python masks for pixel perfect detection. https://www.pygame.org/docs/ref/mask.html
    def collide (self, sprite):
        sprite_mask = sprite.get_mask()
        obs_top_mask = pygame.mask.from_surface(self.OBSTACLE_TOP)
        obs_bottom_mask = pygame.mask.from_surface(self.OBSTACLE_BOTTOM)

        #Calculate offset = Checking if pixels in mask arrays collide. 
        obs_top_offset = (self.x - sprite.x, self.top - round(sprite.y))
        obs_bottom_offset = (self.x - sprite.x, self.bottom - round(sprite.y))

        obs_top_collision_check = sprite_mask.overlap(obs_bottom_mask, obs_bottom_offset)
        obs_bottom_collision_check = sprite_mask.overlap(obs_top_mask, obs_top_offset)

        if obs_top_collision_check or obs_bottom_collision_check:
            return True
        return False

#Move floor sprite and redraw to simulate moving background.
class Floor:
    VEL = 5
    WIDTH = FLOOR_IMG.get_width()
    img = FLOOR_IMG
    
    def __init__(self, y):
        self.y = y
        self.floor1x = 0
        self.floor2x = self.WIDTH

    def move(self):
        self.floor1x -= self.VEL
        self.floor2x -= self.VEL

        #If the x pos of the first floor sprite reaches the end of the left window ie. x <= 0
        #then redraw on top of the current position of the second floor sprite plus move
        #it's x position positively to place it exactly behind the second image vice versa.
        if self.floor1x + self.WIDTH < 0:
            self.floor1x = self.floor2x + self.WIDTH

        if self.floor2x + self.WIDTH < 0:
            self.floor2x = self.floor1x + self.WIDTH

    def draw(self, win):
        win.blit(self.img, (self.floor1x, self.y))
        win.blit(self.img, (self.floor2x, self.y))
    


#Function to draw to window.
def draw_window(win, sprites, obstacles, floor, score):
    win.blit(BACKGROUND_IMG, (0,0))

    for obstacle in obstacles:
        obstacle.draw(win)

    score_text = SCORE_FONT.render("Points: " + str(score), True, (255,255,255))
    win.blit(score_text, (WIN_WIDTH - 10 - score_text.get_width(), 10))

    floor.draw(win)

    for sprite in sprites:
        sprite.draw(win)

    pygame.display.update()

#Main game loop.
def main(genomes, config):
    nets = []
    gen = []
    sprites = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        sprites.append(Floppy_Bird(230, 350))
        g.fitness = 0
        gen.append(g)

    floor = Floor(730)
    obstacles = [Obstacle(random.randrange(500,700))]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock_rate = pygame.time.Clock()
    score = 0

    #Begin Main game loop
    run_game = True
    while run_game:
        clock_rate.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False
                pygame.quit()
                quit()

        #Check which obstacle the neural net should focus on in case of multiple obstacles on window.
        obstacle_index = 0
        if len(sprites) > 0:
            if len(obstacles) > 1 and sprites[0].x > obstacles[0].x + obstacles[0].OBSTACLE_TOP.get_width():
                obstacle_index = 1
        else:
            run_game = False
            break

        #Move the sprite forward and increase its fitness to encourage behaviour.
        for index, sprite in enumerate(sprites):
            sprite.move()
            gen[index].fitness += 0.1

            #Evaluates output according to tanh function.
            output = nets[index].activate((sprite.y, abs(sprite.y - obstacles[obstacle_index].height), abs(sprite.y - obstacles[obstacle_index].bottom)))

            #If the output evaluates to > then 0.5 then we want the sprite to jump.
            if output[0] > 0.5:
                sprite.jump()

        add_obstacle = False
        remove_sprites = []

        for obstacle in obstacles:
            for index, sprite in enumerate(sprites):
                if obstacle.collide(sprite):
                    #This ensures that if more than one sprite reaches the same x-position, if one sprite hits the obstacle then it will have a lower 
                    #fitness than the other sprite which didn't hit the obstacle.
                    gen[index].fitness -= 1
                    sprites.pop(index)
                    nets.pop(index)
                    gen.pop(index)

                #Check if sprite has passed obstacle. If true generate new obstacle.
                if not obstacle.passed and obstacle.x < sprite.x:
                    obstacle.passed = True
                    add_obstacle = True

            #Check if obstacle is off screen.
            if obstacle.x + obstacle.OBSTACLE_TOP.get_width() < 0:
                remove_sprites.append(obstacle)

            obstacle.move()

        if add_obstacle:
            score += 1
            for g in gen:
                g.fitness += 5
            obstacles.append(Obstacle(random.randrange(500,700)))
            add_obstacle = False

        #Remove sprites
        for r in remove_sprites:
            obstacles.remove(r)

        #Check if sprite hits floor or ceiling and terminate them.
        for index, sprite in enumerate(sprites):
            if sprite.y + sprite.sprite.get_height() >= 730 or sprite.y < 0:
                sprites.pop(index)
                nets.pop(index)
                gen.pop(index)

            
        floor.move()
        draw_window(win, sprites, obstacles, floor, score) 

def run(config_path):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    population = neat.Population(config)

    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    winner = population.run(main,1000)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,"config-feedforward.txt")
    run(config_path)


