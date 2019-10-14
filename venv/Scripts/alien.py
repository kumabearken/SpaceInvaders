import pygame
from pygame.sprite import Sprite
import os

class Alien(Sprite):
    '''A class to represent a single alien in the fleet.'''

    def __init__(self, ai_settings, screen, brand):
        '''Iniitialize the alien and set its starting position.'''
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.brand = brand
        self.counter = 0
        self.index=0
        self.exIn = 2
        self.kill = False
        self.exploding = False

        # Load the alien image and set its rect attribute.
        if brand == 0:
            self.images = [pygame.image.load('images/Alien10.png'), pygame.image.load('images/Alien11.png')]
            self.score = 45
        elif brand == 1:
            self.images = [pygame.image.load('images/Alien20.png'), pygame.image.load('images/Alien21.png')]
            self.score = 30
        elif brand == 2:
            self.images = [pygame.image.load('images/Alien30.png'), pygame.image.load('images/Alien31.png')]
            self.score = 15
        self.images.append(pygame.image.load('images/alien_explosion0.png'))
        self.images.append(pygame.image.load('images/alien_explosion1.png'))
        self.images.append(pygame.image.load('images/alien_explosion2.png'))
        self.index = 0
        self.image = self.images[self.index]
        self.image = pygame.transform.scale(self.image, (60, 58))
        self.rect = self.image.get_rect()
        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact postion.
        self.x = float(self.rect.x)

    def blitme(self):
        '''Draw the alien at its current location.'''
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        '''Return True if alien is at edge of screen.'''
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left<= 0:
            return True


    def update(self):
        '''Move the alien right or left.'''
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x
        self.counter += .05
        if(self.exploding):
            if (self.counter >= 1.0):
                self.exIn += 1
                if self.exIn >= 5:
                    self.kill = True
                    self.exploding = False
                    self.exIn=4
                self.image = self.images[self.exIn]
                self.image = pygame.transform.scale(self.image, (60, 58))
                self.counter = 0
            else:
                self.image = self.images[self.exIn]
                self.image = pygame.transform.scale(self.image, (60, 58))
        else:
            if(self.counter >= 1.0):
                self.index += 1
                if self.index >= 2:
                    self.index = 0
                self.image = self.images[self.index]
                self.image = pygame.transform.scale(self.image, (60, 58))
                self.counter = 0
            else:
                self.image = self.images[self.index]
                self.image = pygame.transform.scale(self.image, (60, 58))
