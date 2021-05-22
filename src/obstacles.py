"""
    Classes for the game
"""

from os import path
import pygame


class Obstacle:
    """Model an obstacle"""

    def __init__(self, img_path, coords):
        self.img = pygame.image.load(img_path)
        self.coords = coords

        self.rect = self.img.get_rect()
        self.rect.topleft = self.coords
        self.scroll_speed = 4
    
    def draw(self, surf, game_over):
        """
            Draw the obstacle on the surface
        """
        surf.blit(self.img, (self.rect.x, self.rect.y))
        
        if not game_over:
            self.rect.x -= self.scroll_speed
    
    def __repr__(self):
        return f"<Obstacle @ {self.coords}>"


class Ground(Obstacle):
    """Ground class"""

    def draw(self, surf, game_over):
        """
            Draw the obstacle on the surface
        """
        surf.blit(self.img, (self.rect.x, self.rect.y))
        
        if not game_over:
            self.rect.x -= self.scroll_speed
            if self.rect.x <= -35:
                self.rect.x += 35

    def __repr__(self):
        return f"<Obstacle => Ground @ {self.coords}>"


class Pipe(Obstacle):
    """Model a pipe"""

    def __init__(self, img_path, coords, flip=False):
        super().__init__(img_path, coords)
        self.x, self.y = self.coords
        gap = 160
        
        if flip:
            self.img = pygame.transform.flip(self.img, False, True)
            self.rect = self.img.get_rect()
            self.rect.bottomleft = (self.x), (self.y - (gap/2))
        else:
            self.rect.topleft = (self.x), (self.y + (gap/2))
        
    def __repr__(self):
        return f"<Obstacle => Pipe @ {self.coords}>"
