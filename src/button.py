"""
    button.py

    Contains Button class
"""

import pygame


class Button:
    """Model a button"""

    def __init__(self, coords, img):
	    self.image = img
	    self.rect = self.image.get_rect()
	    self.rect.topleft = coords

    def draw(self, surf):
        action = False

        # Get mouse position
        pos = pygame.mouse.get_pos()

		# Check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

		# Draw button
        surf.blit(self.image, (self.rect.x, self.rect.y))

        return action
