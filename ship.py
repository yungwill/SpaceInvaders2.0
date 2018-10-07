import pygame
from pygame.sprite import Sprite


class Ship(Sprite):

    def __init__(self, ai_settings, screen, stats):
        """Initializes the ship and sets its starting position"""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.stats = stats

        self.index = 0
        self.delay = 0
        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/Ship2.bmp')
        self.death_img = {0: 'images/explosion1.bmp',
                          1: 'images/explosion2.bmp',
                          2: 'images/explosion3.bmp',
                          3: 'images/explosion4.bmp',
                          4: 'images/explosion1.bmp',
                          5: 'images/explosion2.bmp',
                          6: 'images/explosion3.bmp',
                          7: 'images/explosion4.bmp'}
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Store a decimal value for the ship's center
        self.center = float(self.rect.centerx)

        # Movement flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Updates the ship's position based on the movement flag"""
        # Update the ship's center value, not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right and not self.stats.ship_hit:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0 and not self.stats.ship_hit:
            self.center -= self.ai_settings.ship_speed_factor

        # Update rect obj from self.center
        self.rect.centerx = self.center

        if self.delay == 15 and self.index < 8 and self.stats.ship_hit:
            self.image = pygame.image.load(self.death_img[self.index])
            self.index += 1
            self.delay = 0
        elif self.index >= 8 and self.stats.ship_hit:
            self.index = 0
            self.image = pygame.image.load('images/Ship2.bmp')
            self.stats.ship_hit = False
        elif self.stats.ship_hit:
            self.delay += 1

    def blitme(self):
        """Draw the ship at its current location"""
        if self.stats.game_active:
            self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Centers the ship on screen"""
        self.center = self.screen_rect.centerx
