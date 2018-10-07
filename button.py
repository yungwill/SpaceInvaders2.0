import pygame.ftfont
from alien import Alien


class Button:

    def __init__(self, screen, msg, ai_settings, alien_bullets, stats):
        """Initializes button attributes"""
        self.screen = screen
        self.ai_settings = ai_settings
        self.alien_bullets = alien_bullets
        self.stats = stats
        self.screen_rect = screen.get_rect()
        self.centerx = self.screen_rect.centerx

        self.alien1 = Alien(ai_settings, screen, 0, self.alien_bullets, stats)
        self.alien2 = Alien(ai_settings, screen, 1, self.alien_bullets, stats)
        self.alien3 = Alien(ai_settings, screen, 2, self.alien_bullets, stats)
        self.alien4 = Alien(ai_settings, screen, 3, self.alien_bullets, stats)

        # Set the dimensions and properties of the button
        self.width, self.height = 200, 50
        self.button_color = (255, 0, 255)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        # Colors
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)

        self.titlefont = pygame.font.SysFont(None, 100)
        self.titlefont2 = pygame.font.SysFont(None, 50)

        self.title = self.titlefont.render("   SPACE", False, self.white)
        self.title2 = self.titlefont.render("INVADERS", False, self.green)

        self.pt1 = self.titlefont2.render(" = 10 PTS", False, self.white)
        self.pt2 = self.titlefont2.render(" = 20 PTS", False, self.white)
        self.pt3 = self.titlefont2.render(" = 30 PTS", False, self.white)
        self.pt4 = self.titlefont2.render(" = ???", False, self.white)

        # Build the button's rect obj and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (self.centerx, 620)

        # Defining
        self.msg_image = None
        self.msg_image_rect = None

        # The button message needs to be prepped only once
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Turn msg into a rendered image and center the text on the button"""
        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw a blank button and then draw the message
        if not self.stats.score_screen_active:
            self.screen.fill(self.button_color, self.rect)
            self.screen.blit(self.msg_image, (self.ai_settings.screen_width / 2.15, 600))

            self.screen.blit(self.title, (self.ai_settings.screen_width / 3, 150))
            self.screen.blit(self.title2, (self.ai_settings.screen_width / 3, 250))

            self.screen.blit(self.pt1, (self.ai_settings.screen_width / 2.3, 365))
            self.screen.blit(self.pt2, (self.ai_settings.screen_width / 2.3, 415))
            self.screen.blit(self.pt3, (self.ai_settings.screen_width / 2.3, 465))
            self.screen.blit(self.pt4, (self.ai_settings.screen_width / 2.3, 515))

            self.alien2.blitme(self.ai_settings.screen_width / 2.7, 350)
            self.alien1.blitme(self.ai_settings.screen_width / 2.7, 400)
            self.alien3.blitme(self.ai_settings.screen_width / 2.7, 450)
            self.alien4.blitme(self.ai_settings.screen_width / 2.78, 500)
