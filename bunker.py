import pygame
from pygame.sprite import Sprite


class Bunker(Sprite):
    def __init__(self, ai_settings, screen):
        """Initializes the bunker and sets its starting position"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.screen_rect = screen.get_rect()

        # Load the bunker image and sets its rect attribute
        self.image = pygame.image.load('images/Bunker.bmp')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width/2
        self.rect.y = self.screen_rect.bottom - 100

    def blitme(self):
        self.screen.blit(self.image, self.rect)
