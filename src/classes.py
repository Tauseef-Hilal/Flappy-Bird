"""
    Classes for the game
"""

from os import path
import pygame


class Obstacle:
    """Model an obstacle"""

    def __init__(self, img_path, coords, scale):
        self.img = pygame.image.load(img_path)
        self.id = pygame.transform.scale(self.img, scale)

        self.rect = pygame.Rect(*coords, *scale)
        self.scroll_speed = 5
    
    def draw(self, surf):
        """
            Draw the obstacle on the surface
        """
        surf.blit(self.id, (self.rect.x, self.rect.y))
        self.rect.x -= self.scroll_speed
        

class Ground(Obstacle):
    """Ground class"""

    def draw(self, surf):
        """
            Draw the obstacle on the surface
        """
        surf.blit(self.id, (self.rect.x, self.rect.y))
        
        self.rect.x -= self.scroll_speed
        if self.rect.x == -30:
            self.rect.x += 30

    def __repr__(self):
        return f"<Obstacle => Ground>"
        
    
