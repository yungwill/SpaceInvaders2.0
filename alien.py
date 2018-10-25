import pygame
import random
from pygame.sprite import Sprite
from alien_bullet import AlienBullet


class Alien(Sprite):
    """A class to represent a single alien in the fleet"""

    def __init__(self, ai_settings, screen, index, alien_bullets, stats):
        """Initializes the alien and sets its starting position"""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.alien_bullets = alien_bullets
        self.stats = stats
        self.screen_rect = screen.get_rect()
        # Flag for animating the aliens
        self.animate = False

        self.delay = 0
        self.delay2 = 0

        self.timer = random.randint(200, 601)

        # Images for the animations
        self.img = {0: 'images/Alien1.bmp',
                    1: 'images/Alien2.bmp',
                    2: 'images/Alien3.bmp',
                    3: 'images/UFO.bmp'}
        self.img2 = {0: 'images/Alien1.5.bmp',
                     1: 'images/Alien2.5.bmp',
                     2: 'images/Alien3.5.bmp'}

        self.index = index

        # Load the alien image and sets its rect attribute
        self.image = pygame.image.load(self.img[self.index])
        self.rect = self.image.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        # Start each new alien near the top left of the screen if it is not an ufo
        if index != 3:
            self.rect.x = self.rect.width
            self.rect.y = self.rect.height
        # Starts ufo off screen
        else:
            self.rect.x = -self.rect.width
            self.rect.y = self.rect.height

        # Stores the alien's exact position
        self.x = float(self.rect.x)

        # Stores points of UFO in a var
        self.font = pygame.font.SysFont(None, 48)
        self.ufo_points = self.font.render(str(round(self.ai_settings.alien4_points)), True, (255, 255, 255))

    def blitme(self, xpos, ypos):
        """Draws the aliens at desired location"""
        self.screen.blit(self.image, (xpos, ypos))

    def check_edges(self):
        """Returns True if alien is at the edge of the screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Move the aliens, animates every 50 loops, and sets up aliens shooting lasers"""
        if self.index == 3:
            self.x += self.ai_settings.ufo_speed_factor
        else:
            self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x

        if self.delay == 50 and self.index != 3:
            if not self.animate:
                self.image = pygame.image.load(self.img2[self.index])
                self.animate = True
            elif self.animate:
                self.image = pygame.image.load(self.img[self.index])
                self.animate = False
            self.delay = 0
        else:
            self.delay += 1

        # Shoots lasers at random intervals
        if self.delay2 == self.timer:
            if len(self.alien_bullets) < self.ai_settings.alien_bullets_allowed:
                new_bullet = AlienBullet(self.ai_settings, self.screen, self.rect.x, self.rect.y)
                self.alien_bullets.add(new_bullet)
            self.delay2 = 0
            self.timer = random.randint(300, 701)
        else:
            self.delay2 += 1

    def ufo_score_blit(self):
        """Draws the ufo's points to the screen"""
        self.screen.blit(self.ufo_points, (480, 59))
