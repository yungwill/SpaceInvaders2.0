import sys
from time import sleep

import pygame
from bullet import Bullet
from alien import Alien
from bunker import Bunker
from alien_explosion import AlienExplosion


def check_keydown_events(event, ai_settings, screen, ship, bullets, stats):
    """Respond to key presses"""
    # Responds if a key is pressed
    if event.key == pygame.K_RIGHT:
        # Moves ship to the right
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_b:
        stats.score_screen_active = False
    elif event.key == pygame.K_q:
        # press q exits the game
        sys.exit()


def fire_bullet(ai_settings, screen, ship, bullets):
    """Fires a bullet if limit not yet reached"""
    # Create a bew bullet and add it to the bullets group
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    """Respond to key releases"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, score_button, ship, aliens_1,
                 aliens_2, aliens_3, ufo, bullets, alien_bullets, bunkers):
    """Respond to key presses and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets, stats)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens_1,
                              aliens_2, aliens_3, ufo, bullets, alien_bullets, bunkers, mouse_x, mouse_y)
            check_score_button(stats, score_button, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens_1, aliens_2, aliens_3,
                      ufo, bullets, alien_bullets, bunkers, mouse_x, mouse_y):
    """Start a new game when player clicks play"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active and not stats.score_screen_active:
        # Reset the game settings
        ai_settings.initialize_dynamic_settings()
        # Hide the mouse cursor
        pygame.mouse.set_visible(False)
        # Reset the game statistics
        stats.reset_stats()
        stats.game_active = True
        ai_settings.music.play(-1)
        # Reset the scoreboard image
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty the list of aliens and bullets
        aliens_1.empty()
        aliens_2.empty()
        aliens_3.empty()
        bullets.empty()
        ufo.empty()
        # Create a new fleet and center the ship
        create_ufo(ai_settings, screen, ufo, alien_bullets, stats)
        create_fleet(ai_settings, screen, ship, aliens_1, aliens_2, aliens_3, alien_bullets, stats)
        create_fleet2(ai_settings, screen, ship, aliens_1, aliens_2, aliens_3, alien_bullets, stats)
        create_fleet3(ai_settings, screen, ship, aliens_1, aliens_2, aliens_3, alien_bullets, stats)
        create_bunker_set(ai_settings, screen, bunkers)

        ship.center_ship()


def check_score_button(stats, score_button, mouse_x, mouse_y):
    """Checks if the score button has been pressed and takes user to high score screen"""
    score_clicked = score_button.rect.collidepoint(mouse_x, mouse_y)
    if score_clicked and not stats.game_active:
        stats.score_screen_active = True


def update_screen(ai_settings, screen, stats, sb, ship, aliens_1, aliens_2, aliens_3,
                  ufo, bullets, alien_bullets, bunkers, play_button, score_button, back_button):
    """Updates images on the screen and flips to new screen"""
    alien = Alien(ai_settings, screen, 3, alien_bullets, stats)
    collisions_ufo = pygame.sprite.groupcollide(bullets, ufo, True, True)

    # Redraws the screen during each pass through the loop
    screen.fill(ai_settings.bg_color)

    # Redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    for alien_bullet in alien_bullets.sprites():
        alien_bullet.draw_bullet()

    # Draws ship, bunkers, aliens, and scores
    ship.blitme()
    bunkers.draw(screen)
    aliens_1.draw(screen)
    aliens_2.draw(screen)
    aliens_3.draw(screen)
    ufo.draw(screen)
    # Draw the score info
    sb.show_score()

    # Checks if ufo had been hit and shows the points it is worth if it is
    if collisions_ufo:
        ai_settings.ufo_sound.stop()
        ai_settings.death_sound.play()
        ai_settings.ufo_hit = True
    if ai_settings.ufo_hit:
        if ai_settings.delay < 201:
            alien.ufo_score_blit()
            ai_settings.delay += 1
        else:
            ai_settings.ufo_hit = False
            ai_settings.delay = 0

    # Plays faster music when there are less aliens
    if not ai_settings.music2play and stats.game_active:
        if len(aliens_1) <= 12 or len(aliens_2) <= 12 or len(aliens_3) <= 12:
            ai_settings.music.stop()
            ai_settings.music2.play(-1)
            ai_settings.music2play = True

    # Draw the play button if game is inactive
    if not stats.game_active and not stats.score_screen_active:
        play_button.draw_button()
        score_button.draw_button()

    # Draws the high score screen
    if not stats.game_active and stats.score_screen_active:
        sb.draw_score_screen()
        back_button.draw_back()

    # Makes the most recently drawn screen visible
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens_1, aliens_2, aliens_3,
                   ufo, bullets, alien_bullets, bunkers):
    """Updates the position of the bullets and gets rid of the old bullets"""
    # Update bullet positions
    bullets.update()
    alien_bullets.update()

    # Get rid of bullets that have disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    for alien_bullet in alien_bullets.copy():
        if alien_bullet.rect.bottom >= ai_settings.screen_height:
            alien_bullets.remove(alien_bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens_1, aliens_2, aliens_3,
                                  ufo, bullets, alien_bullets, bunkers)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens_1, aliens_2, aliens_3,
                                  ufo, bullets, alien_bullets, bunkers):
    """Respond to bullet-alien collisions"""
    # Remove any bullets and aliens that have collided
    collisions_1 = pygame.sprite.groupcollide(bullets, aliens_1, True, True)
    collisions_2 = pygame.sprite.groupcollide(bullets, aliens_2, True, True)
    collisions_3 = pygame.sprite.groupcollide(bullets, aliens_3, True, True)

    collisions_enemy = pygame.sprite.spritecollide(ship, alien_bullets, True)
    collisions_ufo = pygame.sprite.groupcollide(bullets, ufo, True, True)

    if collisions_1:
        # Plays the death sound
        ai_settings.death_sound.play()
        for aliens in collisions_1.values():
            for alien in aliens:
                # displays explosion of alien
                update_alien_death(ai_settings, screen, stats, sb, ship, aliens_1, aliens_2, aliens_3,
                                   ufo, bullets, alien_bullets, bunkers, 0, alien.rect.x, alien.rect.y)
            # Updates the score
            stats.score += ai_settings.alien1_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if collisions_2:
        # Plays the death sound
        ai_settings.death_sound.play()
        for aliens in collisions_2.values():
            for alien in aliens:
                update_alien_death(ai_settings, screen, stats, sb, ship, aliens_1, aliens_2, aliens_3,
                                   ufo, bullets, alien_bullets, bunkers, 1, alien.rect.x, alien.rect.y)
            stats.score += ai_settings.alien2_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if collisions_3:
        # Plays the death sound
        ai_settings.death_sound.play()
        for aliens in collisions_3.values():
            for alien in aliens:
                update_alien_death(ai_settings, screen, stats, sb, ship, aliens_1, aliens_2, aliens_3,
                                   ufo, bullets, alien_bullets, bunkers, 2, alien.rect.x, alien.rect.y)
            stats.score += ai_settings.alien3_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    # Checks if bullet hit ufo
    if collisions_ufo:
        # Plays the death sound
        ai_settings.ufo_sound.stop()
        ai_settings.death_sound.play()
        for aliens in collisions_ufo.values():
            # Updates the scores
            stats.score += ai_settings.alien4_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    # Checks if the entire fleet is destroyed, start a new level
    if len(aliens_1) == 0 and len(aliens_2) == 0 and len(aliens_3) == 0:
        bullets.empty()
        alien_bullets.empty()
        ai_settings.increase_speed()

        # Increase level
        stats.level += 1
        sb.prep_level()
        ai_settings.music2.stop()
        ai_settings.music2play = False
        ai_settings.music.play(-1)
        create_ufo(ai_settings, screen, ufo, alien_bullets, stats)
        create_fleet(ai_settings, screen, ship, aliens_1, aliens_2, aliens_3, alien_bullets, stats)
        create_fleet2(ai_settings, screen, ship, aliens_1, aliens_2, aliens_3, alien_bullets, stats)
        create_fleet3(ai_settings, screen, ship, aliens_1, aliens_2, aliens_3, alien_bullets, stats)

    # Checks if alien lasers have hit the ship and starts over if true
    if collisions_enemy:
        ship_hit(ai_settings, screen, stats, sb, ship, aliens_1, aliens_2, aliens_3,
                 ufo, bullets, alien_bullets, bunkers)


def get_number_aliens_x(ai_settings, alien_width):
    """Determines the number of aliens that fit in a row"""
    available_space_x = ai_settings.screen_width - 1.2 * alien_width
    number_aliens_x = int(available_space_x / (1.2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determines the number of rows of aliens that fit on the bottom of the screen"""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens_1, aliens_2, aliens_3, alien_number, row_number,
                 indx, alien_bullets, stats):
    """Create an alien and place it in the row"""
    index = indx
    alien = Alien(ai_settings, screen, index, alien_bullets, stats)
    alien_width = alien.rect.width
    alien.x = alien_width + 1.2 * alien_width * alien_number
    alien.rect.x = alien.x
    # Checks the type of alien and adds that type to its fleet
    if indx == 0:
        alien.rect.y = alien.rect.height + 1.2 * alien.rect.height * (3 + row_number)
        aliens_1.add(alien)
    elif indx == 1:
        alien.rect.y = alien.rect.height + 1.2 * alien.rect.height * (1 + row_number)
        aliens_2.add(alien)
    elif indx == 2:
        alien.rect.y = alien.rect.height + 1.2 * alien.rect.height * (5 + row_number)
        aliens_3.add(alien)


def create_fleet(ai_settings, screen, ship, aliens_1, aliens_2, aliens_3, alien_bullets, stats):
    """Create a full fleet of aliens of a single type"""
    # Create an alien and find the number of the aliens in a row
    index = 0
    alien = Alien(ai_settings, screen, index, alien_bullets, stats)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Create fleet of aliens
    for row_number in range(int(number_rows/3)):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens_1, aliens_2, aliens_3,
                         alien_number, row_number, index, alien_bullets, stats)


def create_fleet2(ai_settings, screen, ship, aliens_1, aliens_2, aliens_3, alien_bullets, stats):
    """Create a full fleet of aliens of a single type"""
    # Create an alien and find the number of the aliens in a row
    index = 1
    alien = Alien(ai_settings, screen, index, alien_bullets, stats)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Create fleet of aliens
    for row_number in range(int(number_rows/3)):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens_1, aliens_2, aliens_3,
                         alien_number, row_number, index, alien_bullets, stats)


def create_fleet3(ai_settings, screen, ship, aliens_1, aliens_2, aliens_3, alien_bullets, stats):
    """Create a full fleet of aliens of a single type"""
    # Create an alien and find the number of the aliens in a row
    index = 2
    alien = Alien(ai_settings, screen, index, alien_bullets, stats)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Create fleet of aliens
    for row_number in range(int(number_rows/3)):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens_1, aliens_2, aliens_3,
                         alien_number, row_number, index, alien_bullets, stats)


def create_ufo(ai_settings, screen, ufo, alien_bullets, stats):
    """Create an ufo at the top of the screen"""
    # Create an alien and find the number of the aliens in a row
    index = 3

    alien = Alien(ai_settings, screen, index, alien_bullets, stats)
    # alien.ufo_sound.play()
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height
    ufo.add(alien)


def check_fleet_edges(ai_settings, aliens_1, aliens_2, aliens_3):
    """Responds appropriately if any aliens have reached an edge"""
    for alien in aliens_1.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens_1, aliens_2, aliens_3)
            return None
    for alien in aliens_2.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens_1, aliens_2, aliens_3)
            return None
    for alien in aliens_3.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens_1, aliens_2, aliens_3)
            return None


def change_fleet_direction(ai_settings, aliens_1, aliens_2, aliens_3):
    """Drop the entire fleet and change the fleet's direction"""
    for alien in aliens_1.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    for alien in aliens_2.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    for alien in aliens_3.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, screen, stats, sb, ship, aliens_1, aliens_2, aliens_3, ufo, bullets, alien_bullets, bunkers):
    """Respond to the sho[ being hit by alien"""
    # Sets ship death sound
    ai_settings.music.stop()
    ai_settings.music2.stop()
    ship_death = pygame.mixer.Sound('Sounds/explosion.wav')
    ship_death.play()

    # displays ship death animation
    update_death_animation(screen, ai_settings, bullets, alien_bullets, ship, bunkers, aliens_1, aliens_2,
                           aliens_3, ufo, sb, stats)
    if stats.ships_left > 0:
        # Decrement ships_left
        stats.ships_left -= 1

        # Update scoreboard
        sb.prep_ships()

        # Empty the list of aliens and bullets
        stats.score = 0
        aliens_1.empty()
        aliens_2.empty()
        aliens_3.empty()
        bullets.empty()
        alien_bullets.empty()
        ufo.empty()
        bunkers.empty()

        # Create a new fleet and center the ship
        create_ufo(ai_settings, screen, ufo, alien_bullets, stats)
        create_fleet(ai_settings, screen, ship, aliens_1, aliens_2, aliens_3, alien_bullets, stats)
        create_fleet2(ai_settings, screen, ship, aliens_1, aliens_2, aliens_3, alien_bullets, stats)
        create_fleet3(ai_settings, screen, ship, aliens_1, aliens_2, aliens_3, alien_bullets, stats)
        create_bunker_set(ai_settings, screen, bunkers)
        ship.center_ship()

        # Pause
        sleep(0.4)
        ai_settings.music.play(-1)
    else:
        # Ends the game completely when out of lives
        aliens_1.empty()
        aliens_2.empty()
        aliens_3.empty()
        bullets.empty()
        alien_bullets.empty()
        ufo.empty()
        bunkers.empty()

        ai_settings.music2play = False
        stats.game_active = False
        pygame.mouse.set_visible(True)
        sleep(1)
        game_over()
        sleep(3)
        # Stops music when game ends
        stop_music()


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens_1, aliens_2, aliens_3,
                        ufo, bullets, alien_bullets, bunkers):
    """Check if any aliens have reached the bottom of the screen"""
    screen_rect = screen.get_rect()
    for alien in aliens_1.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treats this the same as if ship got hit
            ship_hit(ai_settings, screen, stats, sb, ship, aliens_1, aliens_2, aliens_3,
                     ufo, bullets, alien_bullets, bunkers)
            break

    for alien in aliens_2.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treats this the same as if ship got hit
            ship_hit(ai_settings, screen, stats, sb, ship, aliens_1, aliens_2, aliens_3,
                     ufo, bullets, alien_bullets, bunkers)
            break

    for alien in aliens_3.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treats this the same as if ship got hit
            ship_hit(ai_settings, screen, stats, sb, ship, aliens_1, aliens_2, aliens_3,
                     ufo, bullets, alien_bullets, bunkers)
            break


def update_aliens(ai_settings, screen, stats, sb, ship, aliens_1, aliens_2, aliens_3,
                  ufo, bullets, alien_bullets, bunkers):
    """Checks if the fleet is at and edge,
    and updates the positions of all the aliens in the fleet"""
    check_fleet_edges(ai_settings, aliens_1, aliens_2, aliens_3)

    aliens_1.update()
    aliens_2.update()
    aliens_3.update()

    # Look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens_1):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens_1, aliens_2, aliens_3,
                 ufo, bullets, alien_bullets, bunkers)

    elif pygame.sprite.spritecollideany(ship, aliens_2):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens_1, aliens_2, aliens_3,
                 ufo, bullets, alien_bullets, bunkers)

    elif pygame.sprite.spritecollideany(ship, aliens_3):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens_1, aliens_2, aliens_3,
                 ufo, bullets, alien_bullets, bunkers)

    # Looks for aliens hitting the bottom of the screen
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens_1, aliens_2, aliens_3,
                        ufo, bullets, alien_bullets, bunkers)


def update_ufo(ai_settings, screen, stats, sb, ship, aliens_1, aliens_2, aliens_3,
               ufo, bullets, alien_bullets, bunkers):
    """Moves the UFO across the screen"""
    ufo.update()
    # Removes ufo when it goes off screen
    for u in ufo.copy():
        if u.rect.x >= 1000:
            ufo.remove(u)
            ai_settings.ufo_sound.stop()
    # Look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, ufo):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens_1, aliens_2, aliens_3,
                 ufo, bullets, alien_bullets, bunkers)


def check_high_score(stats, sb):
    """Check to see if there's a new high score"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def play_music(stats):
    """Plays background music when game starts"""
    music = pygame.mixer.Sound('Sounds/bkgrdmusic.wav')
    if stats.game_active:
        music.play(-1)


def stop_music():
    """Stops all sounds"""
    pygame.mixer.stop()


def game_over():
    """Plays game over sound"""
    gameover = pygame.mixer.Sound('Sounds/gameover.wav')
    gameover.play()


def get_number_bunkers_x(ai_settings, bunker_width):
    """Determines the number of bunkers that fit in a row"""
    available_space_x = ai_settings.screen_width - bunker_width
    number_bunkers_x = int(available_space_x / bunker_width)
    return number_bunkers_x


def create_bunker(ai_settings, screen, bunkers, bunker_number):
    """Create a bunker and place it in the row"""
    bunker = Bunker(ai_settings, screen)
    bunker_width = bunker.rect.width
    bunker.x = bunker_width + 3.25 * bunker_width * bunker_number
    bunker.rect.x = bunker.x/2
    bunker.rect.y = bunker.rect.height * 4
    bunkers.add(bunker)


def create_bunker_set(ai_settings, screen, bunkers):
    """Create a series of bunkers"""
    bunker = Bunker(ai_settings, screen)
    number_bunker_x = get_number_bunkers_x(ai_settings, bunker.rect.width)

    # Create a set of bunkers
    for bunker_number in range(number_bunker_x):
        create_bunker(ai_settings, screen, bunkers, bunker_number)


def update_death_animation(screen, ai_settings, bullets, alien_bullets, ship, bunkers, aliens_1, aliens_2,
                           aliens_3, ufo, sb, stats):
    """Allows the ship to animate its death explosion when a cycle has not completed to update the screen"""
    stats.ship_hit = True
    while stats.ship_hit:
        ship.update()
        if stats.ship_hit:
            screen.fill(ai_settings.bg_color)
            # Redraw all bullets behind ship and aliens
            for bullet in bullets.sprites():
                bullet.draw_bullet()
            for alien_bullet in alien_bullets.sprites():
                alien_bullet.draw_bullet()
            ship.blitme()
            bunkers.draw(screen)
            aliens_1.draw(screen)
            aliens_2.draw(screen)
            aliens_3.draw(screen)
            ufo.draw(screen)
            # Draw the score info
            sb.show_score()

            pygame.display.flip()


def update_alien_death(ai_settings, screen, stats, sb, ship, aliens_1, aliens_2, aliens_3,
                       ufo, bullets, alien_bullets, bunkers, index, x, y):
    """Allows the aliens to animate its death explosion when a cycle has not completed to update the screen"""
    alien = Alien(ai_settings, screen, 3, alien_bullets, stats)
    explosion = AlienExplosion(ai_settings, screen, index, stats, x, y)
    stats.alien_hit[index] = True
    while stats.alien_hit[index]:
        explosion.update()

        collisions_ufo = pygame.sprite.groupcollide(bullets, ufo, True, True)
        # Redraws the screen during each pass through the loop
        screen.fill(ai_settings.bg_color)
        # Redraw all bullets behind ship and aliens
        for bullet in bullets.sprites():
            bullet.draw_bullet()
        for alien_bullet in alien_bullets.sprites():
            alien_bullet.draw_bullet()
        ship.blitme()
        bunkers.draw(screen)
        aliens_1.draw(screen)
        aliens_2.draw(screen)
        aliens_3.draw(screen)
        ufo.draw(screen)
        # Draw the score info
        sb.show_score()

        explosion.blitme()

        if collisions_ufo:
            ai_settings.death_sound.play()
            ai_settings.ufo_hit = True
        if ai_settings.ufo_hit:
            if ai_settings.delay < 201:
                alien.ufo_score_blit()
                ai_settings.delay += 1
            else:
                ai_settings.ufo_hit = False
                ai_settings.delay = 0

        pygame.display.flip()
