import pygame

from pygame.sprite import Sprite


class AlienBullet(Sprite):
    """A class to manage the alien bullets fired from the aliens"""

    def __init__(self, ai_settings, screen, x_pos, y_pos):
        """Create a bullet obj at the aliens's current position"""
        super().__init__()
        self.screen = screen
        self.x_pos, self.y_pos = x_pos, y_pos
        # Create a bullet rect at (0, 0) and then set correct position
        self.rect = pygame.Rect(x_pos, y_pos, ai_settings.bullet_width,
                                ai_settings.bullet_height)

        # Store the bullet's position as a decimal value
        self.y = float(self.rect.y)

        self.color = ai_settings.alien_bullet_color
        self.speed_factor = ai_settings.alien_bullet_speed_factor
        # Loads shooting sound
        self.laser_sound = pygame.mixer.Sound('Sounds/shoot.wav')
        # Plays the shooting sound
        self.laser_sound.play()

    def update(self):
        """Move the bullet down the screen"""
        # Update the decimal position of the bullet
        self.y += self.speed_factor
        # Update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
