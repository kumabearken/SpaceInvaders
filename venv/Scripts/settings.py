class Settings():
    '''A class to store all settings for Alien invasiom.'''

    def __init__(self):
        '''Initialize the games's settings.'''
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (50, 50, 50)

        # Ship settings
        self.ship_speed_factor = 1.5
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 255,99,99
        self.bullets_allowed = 100

        # Alien setting
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10

        #Bunker Setting
        self.size = 150
        self.color = (255,255,255)

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        # How quickly the alien point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

    def update(self):
        '''Move the alien ri0ht.'''
        self.x += self.ai_settings.alien_speed_factor
        self.rect.x = self.x

    def initialize_dynamic_settings(self):
        '''Initialize settings that change throught the game.'''
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        '''Increase speed settings and alien point values..'''
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)