import pygame

from pygame.sprite import Sprite


class AlienExplosion(Sprite):
    """A class to animate the explosion of an alien when it dies"""
    def __init__(self, ai_settings, screen, index, stats, xpos, ypos):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.stats = stats
        self.index = index
        self.xpos = xpos
        self.ypos = ypos
        self.screen_rect = screen.get_rect()

        # All the images needed for the animation of each type of alien
        self.alien1_death_img = {0: 'images/alien1_explosion1.bmp',
                                 1: 'images/alien1_explosion2.bmp',
                                 2: 'images/alien1_explosion3.bmp'}

        self.alien2_death_img = {0: 'images/alien2_explosion1.bmp',
                                 1: 'images/alien2_explosion2.bmp',
                                 2: 'images/alien2_explosion3.bmp'}

        self.alien3_death_img = {0: 'images/alien3_explosion1.bmp',
                                 1: 'images/alien3_explosion2.bmp',
                                 2: 'images/alien3_explosion3.bmp'}

        # A count so that the animation loops all the way through
        self.index2 = 0
        self.index3 = 0
        self.index4 = 0

        self.image = None

    def update(self):
        """Updates the image needed to be shown"""

        # Checks if the index is inside the range for the images, checks which alien type it is
        # Checks if that alien has been hit and if all are true then the image changes to the next one
        # Ends when the index hits 3
        if self.index2 < 3 and self.index == 0 and self.stats.alien_hit[0]:
            self.image = pygame.image.load(self.alien1_death_img[self.index2])
            self.index2 += 1
        elif self.index2 >= 3 and self.stats.alien_hit[0]:
            self.index2 = 0
            self.stats.alien_hit[0] = False

        if self.index3 < 3 and self.index == 1 and self.stats.alien_hit[1]:
            self.image = pygame.image.load(self.alien2_death_img[self.index3])
            self.index3 += 1
        elif self.index3 >= 3 and self.stats.alien_hit[1]:
            self.index3 = 0
            self.stats.alien_hit[1] = False

        if self.index4 < 3 and self.index == 2 and self.stats.alien_hit[2]:
            self.image = pygame.image.load(self.alien3_death_img[self.index4])
            self.index4 += 1
        elif self.index4 >= 3 and self.stats.alien_hit[2]:
            self.index4 = 0
            self.stats.alien_hit[2] = False

    def blitme(self):
        """Draws the explosion at its current location"""
        self.screen.blit(self.image, (self.xpos, self.ypos))
