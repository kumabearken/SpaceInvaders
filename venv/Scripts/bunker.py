import pygame
from pygame.sprite import Sprite

class Bunker(Sprite):
    def __init__(self, ai_settings, screen):
        '''Initialize the ship and set its starting position.'''
        super(Bunker, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/Bunk1.png')
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship at bottom center of the screen.
        self.rect.centerx = 600
        self.rect.bottom = self.screen_rect.bottom - 100

        # Store a decimal valiue for the ship's center.
        self.center = float(self.rect.centerx)

    def blitme(self):
        self.screen.blit(self.image, self.rect)
    
    def update(self, x, y):
        self.rect.x = 750
        self.rect.y = 750
        print(self.rect.x)