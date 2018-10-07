import random
import pygame


class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initializes the game's static settings"""
        # Screen settings
        self.screen_width = 1000
        self.screen_height = 800
        # Sets background color
        self.bg_color = (0, 0, 0)

        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 255, 0, 0
        self.alien_bullet_color = 255, 255, 0
        self.alien_bullets_allowed = 6
        self.bullets_allowed = 10

        self.music = pygame.mixer.Sound('Sounds/bkgrdmusic.wav')
        self.music1 = pygame.mixer.Sound('Sounds/bkgrdmusic1.25.wav')
        self.music2 = pygame.mixer.Sound('Sounds/bkgrdmusic1.5.wav')
        self.death_sound = pygame.mixer.Sound('Sounds/invaderkilled.wav')
        self.ufo_sound = pygame.mixer.Sound('Sounds/ufo_lowpitch.wav')

        self.music1play = False
        self.music2play = False
        self.ufo_hit = False

        self.delay = 0

        # Alien settings
        self.fleet_drop_speed = 10

        # How quickly the game speeds up
        self.speedup_scale = 1.1
        # How quickly the alien point values increase
        self.score_scale = 1.5
        self.sound_speedup = 1.1

        self.ship_speed_factor = None
        self.bullet_speed_factor = None
        self.alien_bullet_speed_factor = None
        self.alien_speed_factor = None
        self.ufo_speed_factor = None
        # fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = None

        # Scoring
        self.alien1_points = 20
        self.alien2_points = 10
        self.alien3_points = 30
        self.alien4_points = round(random.randint(100, 301))

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initializes settings that change throughout the game"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 1.5
        self.alien_bullet_speed_factor = .7
        self.alien_speed_factor = .5
        self.ufo_speed_factor = 3
        # fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase speed settings and alien point values"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.ufo_speed_factor *= self.speedup_scale
