import pygame
import random
from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from score_button import ScoreButton
from ship import Ship
import game_functions as gf


def run_game():
    # Initializes background setting needed to run properly
    pygame.init()

    # Initializes settings
    ai_settings = Settings()

    # Creates a display window where all of the game's graphic elements are drawn
    # The numbers represent the dimensions of the window
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Delay time
    delay = 0
    timer = random.randint(400, 1001)

    # Create an instance to store game statistics amd create a scoreboard
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Makes a ship, group of bullets, alien bullets, group of aliens, and ufos
    ship = Ship(ai_settings, screen, stats)
    bunkers = Group()
    bullets = Group()
    aliens_1 = Group()
    aliens_2 = Group()
    aliens_3 = Group()
    alien_bullets = Group()
    ufo = Group()

    # Make the play button that also contains the startup screen
    play_button = Button(screen, "Play", ai_settings, alien_bullets, stats)
    score_button = ScoreButton(screen, "High Scores", ai_settings)
    back_button = ScoreButton(screen, "Back (B)", ai_settings)

    # Starts the main loop for the game
    while True:
        # Checks for any type of event
        gf.check_events(ai_settings, screen, stats, sb, play_button, score_button, ship, aliens_1,
                        aliens_2, aliens_3, ufo, bullets, alien_bullets, bunkers)

        # Creates a new UFO at a random interval
        # Delay to prevent too many from spawning at once
        if delay == timer:
            gf.create_ufo(ai_settings, screen, ufo, alien_bullets, stats)
            # plays ufo sound
            ai_settings.ufo_sound.play()
            delay = 0
            timer = random.randint(700, 1001)
        else:
            delay += 1

        # Runs the game is active
        if stats.game_active:
            ship.update()

            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens_1, aliens_2, aliens_3,
                              ufo, bullets, alien_bullets, bunkers)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens_1, aliens_2, aliens_3,
                             ufo, bullets, alien_bullets, bunkers)
            gf.update_ufo(ai_settings, screen, stats, sb, ship, aliens_1, aliens_2, aliens_3,
                          ufo, bullets, alien_bullets, bunkers)
        # Manages the screen updates
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens_1, aliens_2, aliens_3, ufo,
                         bullets, alien_bullets, bunkers, play_button, score_button, back_button)


run_game()
