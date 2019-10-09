import pygame
from pygame.sprite import Sprite
import random

class UFO(Sprite):
    '''A class to represent a single alien in the fleet.'''

    def __init__(self, ai_settings, screen):
        '''Iniitialize the alien and set its starting position.'''
        super(UFO, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load('images/UFO1.png')
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()


        # Start each new alien near the top left of the screen.
        self.rect.top = 25
        self.rect.right = random.randint(-5000,-300)

        # Store the alien's exact postion.
        self.x = float(self.rect.x)

    def blitme(self):
        '''Draw the alien at its current location.'''
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        '''Return True if alien is at edge of screen.'''
        screen_rect = self.screen.get_rect()
        if self.rect.left >= screen_rect.right:
            return True

    def update(self):
        '''Move the alien right or left.'''
        self.x += (self.ai_settings.alien_speed_factor)
        self.rect.x = self.x

    def hit(self):
        self.rect.left = 1200
        self.blitme()