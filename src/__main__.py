"""
    __main__.py
"""

from os import path
from random import choice
import pygame
from src.classes import Ground

# Set up game window
WIDTH, HEIGHT = 400, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Set up Clock
CLOCK = pygame.time.Clock()
FPS = 60

# Ground obj
GROUND = Ground(path.join("sprites", "base.png"), (0, 512), (WIDTH+30, 88))

# Backgrounds
IMG_1 = pygame.image.load(path.join("sprites", "background-day.png"))
IMG_2 = pygame.image.load(path.join("sprites", "background-night.png"))
DAY = pygame.transform.scale(IMG_1, (WIDTH, 512))
NIGHT = pygame.transform.scale(IMG_2, (WIDTH, 512))
BACKGROUNDS = [DAY, NIGHT]


def draw(background):
    WIN.blit(background, (0, 0))
    GROUND.draw(WIN)
    pygame.display.update()
    CLOCK.tick(FPS)


def main():
    """ Main function """
    background = choice(BACKGROUNDS)

    game_on = True
    while game_on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_on = False
                pygame.quit()
        
        draw(background)


if __name__ == "__main__":
    main()
