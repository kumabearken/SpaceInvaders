import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien
from bunker import Bunker
from ufo import UFO
import random
from tkinter import *
import os
from window import takeInput


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    '''Respond to keypresse.'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''Check if any aliens have reached the bottom of the screen.'''
    screen_rect = screen.get_rect()
    for alien in aliens:
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break


def check_high_score(stats, sb):
    '''Check to see if there's a new hgih score.'''
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def check_keyup_events(event, ship):
    '''Respond to key releases.'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, bunkers,ufos):
    '''Respond to keypresses and mouse events.'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y, bunkers, ufos)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets,  mouse_x, mouse_y, bunkers,ufos):
    '''Start a new game when the player clicks Play.'''
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings.
        ai_settings.initialize_dynamic_settings()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

        # Reset the game statistics.
        stats.reset_stats()
        stats.game_active =True

        # Reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty the lists of aliens and bullets.
        aliens[:] = []
        bullets.empty()
        ufos.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens, stats)
        create_bunkers(ai_settings, screen, bunkers)
        create_ufo(ai_settings,screen,ufos)
        ship.center_ship()


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets,bunkers,ufos):
    '''Respind to bullet-alien collisions'''
    # Remove any bullets and aliens that have collided.
    counter = 0
    for alien in aliens:
        ++counter
        collisions = pygame.sprite.spritecollide(alien, bullets, True)
        if collisions:
            effect = pygame.mixer.Sound('sounds\\alien.wav')
            effect.play()
            stats.score += alien.score
            sb.prep_score()
            print(alien.score)
            aliens.remove(alien)
        check_high_score(stats, sb)
    #collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    #counter = 0
    #if collisions:
    #    for aliens in collisions.values():
    #        stats.score += ai_settings.alien_points * len(aliens)
    #        sb.prep_score()
    #    check_high_score(stats, sb )
    if len(aliens) == 0:
        # If entire fleet is destroyed start a new level.
        bullets.empty()
        ai_settings.increase_speed()
        ufos.empty()
        # Increase level.
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens, stats)
        create_bunkers(ai_settings,screen, bunkers)
        create_ufo(ai_settings, screen, ufos)



def check_bullet_ufo_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets,bunkers,ufos):
    '''Respind to bullet-alien collisions'''
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(ufos, bullets, True, True)
    if collisions:
        effect = pygame.mixer.Sound('sounds\\alien.wav')
        effect.play()
        points = random.randint(1,100)*100
        sb.prep_ufo(points)
        stats.score += points
        sb.prep_score()
        check_high_score(stats, sb )

def check_bullet_bunker_collisions(ai_settings, screen, stats, sb, ship, bunkers, bullets):
    '''Respind to bullet-alien collisions'''
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, bunkers, True, True)
    if collisions:
        for bunkers in collisions.values():
           1+1 #need to do pill thing


def check_fleet_edges(ai_settings, aliens):
    '''Respond appropriately if any aliens have reached an edge.'''
    for alien in aliens:
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    '''Drop the entire fleet and change the fleet's direction.'''
    for alien in aliens:
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def create_alien(ai_settings, screen, aliens, alien_number, row_number, index, stats):
    '''Create an alien and place it in the row.'''
    if row_number == 0:
        alien = Alien(ai_settings, screen, 0)
    elif row_number == 1 or row_number == 2:
        alien = Alien(ai_settings, screen, 1)
    else:
        alien = Alien(ai_settings, screen, 2)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 1 * alien.rect.height * row_number + 150
    alien.index = index
    alien.score = alien.score * stats.level
    aliens.append(alien)


def create_bunkers(ai_settings, screen, bunkers):
    number_bunker_x = get_number_bunker_x(ai_settings, 100)
    for bunker_number in range(number_bunker_x-1):
        bunker = Bunker(ai_settings, screen)
        bunker.rect.centerx = bunker_number * 300 + 150
        bunker.rect.bottom = bunker.rect.bottom
        bunkers.add(bunker)


def create_ufo(ai_settings, screen, ufos):
    '''Create an alien and place it in the row.'''
    if len(ufos) < 1 :
        ufo = UFO(ai_settings, screen)
        ufos.add(ufo)


def create_fleet(ai_settings, screen, ship, aliens, stats):
    '''Create a full fleet of aliens.'''
    # Create an alien and find the number of aliens in a row,
    # Spacing between each alien is equal to one alien width.
    alien = Alien(ai_settings, screen, 0)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    number_rows = 5
    index = 0
    # Create the fleet of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number, index, stats)
            ++index


def fire_bullet(ai_settings, screen, ship, bullets):
    '''Fire a bullet if limt not reached yet.'''
    # Create a new bullet and add it to the bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        effect = pygame.mixer.Sound('sounds\laser.wav')
        effect.play()
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_aliens_x(ai_settings, alien_width):
        '''Determine the number of aliens that fit in a row.'''
        available_space_x = ai_settings.screen_width - 2 * alien_width
        number_aliens_x = int(available_space_x / (2 * alien_width))
        return number_aliens_x


def get_number_bunker_x(ai_settings, bunker_width):
    '''Determine the number of aliens that fit in a row.'''
    available_space_x = ai_settings.screen_width - 2 * bunker_width
    number_bunker_x = int(available_space_x / (2 * bunker_width))
    return number_bunker_x


def get_number_rows(ai_settings, ship_height, alien_height):
    '''Determine the number of rows of aliens that fit on the screen.'''
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def getText(requestMessage):
    go = True
    while(go):
        msgBox = takeInput(requestMessage)
        # loop until the user makes a decision and the window is destroyed
        msgBox.waitForInput()
        name = msgBox.getString()
        if(name == ''):
            blank =0
        else:
            go=False
    return name

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
     '''Respind to the ship being hit by alien'''
     if stats.ships_left > 0:
        # Decrement ships_left.
        stats.ships_left -= 1
        effect = pygame.mixer.Sound('sounds\\ship.wav')
        effect.play()
        for x in range(0,10):
            ship.ship_explode(x)
            ship.screen.blit(ship.image, ship.rect)
            pygame.display.flip()
        # Update scoreboard.
        sb.prep_ships()
        # Empty the lists of aliens and fullets.
        aliens[:]=[]
        bullets.empty()
        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens, stats)
        ship.center_ship()
        # Pause.
        ship.ship_explode(10)
     else:
         stats.game_active = False
         pygame.mouse.set_visible(True)
         update_highscore(stats.score)


def update_bunkers(bunkers, screen):
    # bunkers.draw(screen)
    for bunker in bunkers:
        bunker.blitme()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, bunkers, ufos):
    '''Update position of bullets and get rid of old bullets'''
    # Update bullet positions.
    bullets.update()

    # Get rid of bullets that have disapperec.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, bunkers,ufos)
    check_bullet_bunker_collisions(ai_settings, screen, stats, sb, ship, bunkers, bullets)
    check_bullet_ufo_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, bunkers, ufos)


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, bunkers,ufos):
    '''Update images on the screen and flip to the new screen.'''
    # Redraw the screen during each pass through the loop.
    screen.fill(ai_settings.bg_color)
    # Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    ufos.draw(screen)
    #aliens.draw(screen)
    for alien in aliens:
        alien.blitme()
    update_bunkers(bunkers, screen)
    # Draw the score information.
    sb.show_score()

    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible.
    pygame.display.flip()


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, clock):
    '''
    Check if the fleet is at an edge
    and then update the positions of all aliens in the fleet.
    '''
    check_fleet_edges(ai_settings, aliens)
    for alien in aliens:
        alien.update()
        #aliens.update()

    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    # Look for aliens hitting the bottom of the screen
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)


def update_highscore(score):
    print("im here")
    currentLine = ""
    tempLine=""
    drop = False
    name =""
    with open("highscore.txt","r") as iFile, open("temp.txt","w") as oFile:
        print("test1")
        for line in iFile:
            print("test2")
            if drop:
                print("drop")
                currentLine = line
                a,b,c = tempLine.split()
                d,e,f = currentLine.split()
                line = d + ' ' + b + ' ' + c + '\n'
                oFile.write(line)
                tempLine = currentLine
            else:
                print("high")
                a,b,c = line.split()
                if (score > int(c)):
                    tempLine = line
                    name = getText('enter name')
                    line = a + " " +  name + " " + str(score) + '\n'
                    oFile.write(line)
                    drop = True
                else:
                    print("no change")
                    oFile.write(line)
    iFile.close()
    oFile.close()
    os.remove('highscore.txt')
    os.rename('temp.txt', 'highscore.txt')
