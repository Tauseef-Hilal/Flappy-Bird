"""
    Bird class
"""

from os import path
import pygame

pygame.mixer.init()
GAME_OVER_SOUND = pygame.mixer.Sound(path.join("sfx", "hit.wav"))


class Bird:
    """Model the Flappy Bird"""

    def __init__(self, img_path, color, coords):
        self.images = []

        for i in range(3):
            image = pygame.image.load(img_path.format(color, i))
            image = pygame.transform.scale(image, (50, 35))
            self.images.append(image)
        
        self.rect = self.images[0].get_rect()
        self.rect.center = coords

        self.index = 0
        self.counter = 0
        self.flap_after = 8                     # Animate after 
        self.g = 0.5                            # Acceleration due to gravity
        self.vel = 0                            # Initial velcocity
        self.max_vel = -8                       # Jump Velocity
        self.clicked = False
        self.times = 0
        self.flying = False
    
    def draw(self, surf, game_over):
        """Display the bird"""
        if not game_over:
            self._animate()
        else:
            if self.times == 0:
                self.current_img = pygame.transform.rotate(self.current_img,
                                                          -90)
                GAME_OVER_SOUND.play()
                self.times = 1
        
        surf.blit(self.current_img, self.rect.center)

        if self.clicked:
            self._jump()
        else:
            if self.flying:
                self._apply_gravity()
    
    def _animate(self):
        """Animate the bird"""

        self.counter += 1
        if self.counter >= self.flap_after:
            self.counter = 0
            self.index += 1
            if self.index > 2:
                self.index = 0
        
        # Rotate the bird
        self.current_img = self.images[self.index]
        self.current_img = pygame.transform.rotate(self.current_img, 
                                                   self.vel * -2)
    
    def _apply_gravity(self):
        """Accelerate the bird downwards"""

        self.vel += self.g
        if self.vel >= -self.max_vel:
            self.vel = -self.max_vel
        
        self._move()
    
    def _jump(self):
        """Trigger jump"""

        self.vel = self.max_vel
        self._move()
    
    def _move(self):
        """Move the bird"""

        if self.clicked:
            if self.rect.top >= 0:
                self.rect.y += self.vel
            
            self.clicked = False
        else:
            if self.rect.bottom <= 490:
                self.rect.y += self.vel

