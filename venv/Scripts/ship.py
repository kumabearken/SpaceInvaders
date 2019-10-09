import pygame
from pygame.sprite import Sprite
from time import sleep

class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        '''Initialize the ship and set its starting position.'''
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/Ship.png')
        self.image = pygame.transform.scale(self.image, (60, 58))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.explode = [pygame.image.load('images/ShipExplosion00.png'),
                   pygame.image.load('images/ShipExplosion01.png'),
                  pygame.image.load('images/ShipExplosion02.png'),
                 pygame.image.load('images/ShipExplosion03.png'),
                pygame.image.load('images/ShipExplosion04.png'),
               pygame.image.load('images/ShipExplosion05.png'),
              pygame.image.load('images/ShipExplosion06.png'),
             pygame.image.load('images/ShipExplosion07.png'),
            pygame.image.load('images/ShipExplosion08.png'),
           pygame.image.load('images/ShipExplosion09.png'),
          pygame.image.load('images/Ship.png')]
        # Start each new ship at bottom center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Store a decimal valiue for the ship's center.
        self.center = float(self.rect.centerx)

        # Movement flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        '''Update the ship's position based on the movement flag.'''
        # Update the ship's center value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # Update rect object from self.center
        self.rect.centerx = self.center

    def blitme(self):
        '''Draw the ship at its current locatio.'''
        self.screen.blit(self.image,self.rect)

    def center_ship(self):
        '''Center the ship on the screen.'''
        self.center = self.screen_rect.centerx

    def ship_explode(self, x):
        self.image = self.explode[x]
        self.image = pygame.transform.scale(self.image, (60, 58))
        sleep(.25)
        print("running")
