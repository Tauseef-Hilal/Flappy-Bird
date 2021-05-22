"""
    __main__.py
"""

from os import path
from random import choice, randint
import pygame
from src.obstacles import Ground, Pipe
from src.bird import Bird

# Set up game window
WIDTH, HEIGHT = 850, 680
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
pygame.display.set_icon(pygame.image.load("flappy.ico"))

# Set up Clock
CLOCK = pygame.time.Clock()
FPS = 60

# Background Music
pygame.mixer.init()
pygame.mixer.music.load(path.join("music", "background.mp3"))
pygame.mixer.music.play(-1)

# Ground
GROUND = Ground(path.join("sprites", "base.png"), (0, HEIGHT-168))

# Bird
BIRDS = ["redbird", "bluebird", "yellowbird"]
COLOR = choice(BIRDS)
BIRD = Bird(path.join("sprites", "{}-{}.png"),
            COLOR, (200, 300))

# Pipes
pipes = []
pipe_img = path.join("sprites", "pipe-green.png")
pipe_delay = 75

# Backgrounds
BACKGROUND = pygame.image.load(path.join("sprites", "background.png"))


def create_pipes(pipe_counter):
    """
        Create pipe objs

        :pipe_counter: Keeps on increasing till it
                       equals the global pipe_delay

        When pipe_counter hits global pipe_delay,
        two pipes get created and pipe_counter
        resets to 0

        For the first time, pipe_counter is -1
        just to create two pipes at the start
        of the game!
    """

    if pipe_counter == pipe_delay or pipe_counter == -1:
        for i in range(2):
            gap = randint(100, 180)
            flip = False
            
            if i == 1:
                gap = -gap
                flip = True

            pipe = Pipe(pipe_img, (WIDTH, (HEIGHT/2 - 100) + gap/2), flip=flip)
            pipes.append(pipe)
        pipe_counter = 0
    else:
        pipe_counter += 1
    
    return pipe_counter


def draw():
    WIN.blit(BACKGROUND, (0, 0))

    for pipe in pipes:
        pipe.draw(WIN)
    
    GROUND.draw(WIN)
    BIRD.draw(WIN)
    pygame.display.update()
    CLOCK.tick(FPS)


def main():
    """ Main function """

    pipe_counter = -1
    game_on = True
    while game_on:
        
        # Create and draw pipes
        pipe_counter = create_pipes(pipe_counter)
        for pipe in pipes:
            if pipe.rect.right < 0:
                pipes.remove(pipe)
                del pipe
                continue

        # Handle events
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                game_on = False
                pygame.quit()
            
            if event.type == pygame.MOUSEBUTTONUP:
                BIRD.clicked = True
        
        # Display the game
        draw()


if __name__ == "__main__":
    main()
