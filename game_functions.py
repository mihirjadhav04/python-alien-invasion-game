import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
    """ Respond to Key press and Mouse events. """

    #Watch for keyboard and mouse events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        #Each event is picked up by the pygame.event.get() method
        #Each keypress is registered as a KEYDOWN event.
        elif event.type == pygame.KEYDOWN: 
            check_keydown_events(event,ai_settings,screen,ship,bullets)

        #We’ll have our game detect a pygame.KEYUP event so we’ll know when the right arrow key is released; then we’ll use the KEYDOWN and KEYUP events together with a flag called moving_right to implement continuous motion.
        
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y)

def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y):
    """Starts a new game when the player clicks the game."""
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active: #Because we want to avoid clicking of play button area after the game starts
        #Reset the game settings
        ai_settings.initialize_dyanamic_settings()

        #Hide the mouse cursor - Passing False to set_visible() tells Pygame to hide the cursor when the mouse is over the game window.
        pygame.mouse.set_visible(False)

        #Reset the game statistics
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        #Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        #Create a new fleet and center the ship.
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()

def check_keydown_events(event,ai_settings,screen,ship,bullets):
    """Respond to the Key Press Event"""
    if event.key == pygame.K_RIGHT: #Check whether the key pressed is right arrow key?
        #Move the ship to the right
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    #check spacebar event for bullet shooting
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings,screen,ship,bullets)
    #checking q button press event for quiting the game instead of using mouse.
    elif event.key == pygame.K_q:
        sys.exit()
        

def check_keyup_events(event,ship):
    """Respond to the Key Release Event"""
    if event.key == pygame.K_RIGHT: #Check whether the key pressed is right arrow key?
        #Move the ship to the right
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button):
    """ Update images on the screen and flip to new screen. """

    #Redraw the screen during each pass pf the loop
    screen.fill(ai_settings.bg_color)

    #Redraw all the bullets behing the ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet() 

    #To display ship.(method call)
    ship.blitme()

    #To display alien
    aliens.draw(screen)
    #Draw the score information
    sb.show_score()

    #Draw the play button if the game is inactive
    if not stats.game_active:
        play_button.draw_button()

    #Make the most recently drawn screen visible.
    pygame.display.flip()


def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
    """Updates position of bullets and get rid of old bullets."""
    #Update bullets position.
    bullets.update()
    #get rid of the bullets that have dissappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    print(len(bullets))

    check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets)

def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets):
    """Respond to bullet alien collision."""
    #Check for any bullet that have hit the alien.
    #if so then get rid of the bullet and alien.
    collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats,sb)


    if len(aliens) == 0:
        #Destroy existing bullets,speedup the game, and create new fleet.
        bullets.empty()
        ai_settings.increase_speed()

        #If entire fleet is destroyed, start a new level
        stats.level += 1    
        sb.prep_level()
        create_fleet(ai_settings,screen,ship,aliens)
    
def fire_bullet(ai_settings,screen,ship,bullets):
    """Fire a bullet if limit not reached yet."""
    #Create a new bullet and add it to the bullets group
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)


def get_number_aliens_x(ai_settings,alien_width):
    """Determine the numeber of alien fit in the row"""
    #Claculating the available screen space to display the aliens.
    available_space_x = ai_settings.screen_width - 2 * alien_width
    #Claculating how many aliens can fit in that space.
    number_aliens_x = int(available_space_x /( 2 * alien_width))

    return number_aliens_x


def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    """Create an alien and place it in the row."""
    #Creating an alien
    alien = Alien(ai_settings,screen)
    #Finding the width of that alien.
    alien_width = alien.rect.width

    alien = Alien(ai_settings,screen)
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings,screen,ship,aliens):
    """Create a full fleet of aliens. """
    
    #Creating an alien
    alien = Alien(ai_settings,screen)

    number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings,screen,aliens,alien_number,row_number)


def get_number_rows(ai_settings,ship_height,alien_height):
    """Determine the number of rows of aliens that fit in the screen"""
    available_space_y = ai_settings.screen_height - (3 * alien_height) - ship_height
    number_rows = int(available_space_y / ( 2 * alien_height))
    return number_rows


def check_fleet_edges(ai_settings,aliens):
    """Respond appropriately if any alien have reached the edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break

def change_fleet_direction(ai_settings,aliens):
    """ Drop the entire fleet and change it's direction """
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_aliens(ai_settings,stats,sb,screen, ship ,aliens,bullets):
    """ Check if the fleet is at teh edge and update the position of all aliens in the fleet."""
    check_fleet_edges(ai_settings,aliens)
    aliens.update()

    #Look for alien ship collison
    if pygame.sprite.spritecollideany(ship,aliens):
        print("Ship Hit !!!")
        ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets)
        """ 
        The method spritecollideany() takes two arguments: a sprite and a
        group. The method looks for any member of the group that’s collided with
        the sprite and stops looping through the group as soon as it finds one mem-
        ber that has collided with the sprite. Here, it loops through the group aliens
        and returns the first alien it finds that has collided with ship .
        """
    #Look for aliens hitting the bottom of the screen
    check_aliens_bottom(ai_settings, stats,sb, screen, ship, aliens, bullets)


def ship_hit(ai_settings, stats,sb, screen, ship, aliens, bullets):
    """Respond to ship being hit by alien."""
    
    if stats.ships_left > 0:
        # Decrement ships_left.
        stats.ships_left -= 1
        
        #Update score
        sb.prep_ships()

        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause.
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
        
def check_aliens_bottom(ai_settings, stats,sb, screen, ship, aliens, bullets):
    """Check if the aliens have reach the bottom of the screen"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #Treat the same way as the ship got hit.
           ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets) 
           break

def check_high_score(stats,sb):
        """Check to see if there's a new high score"""
        if stats.score > stats.high_score:
            stats.high_score = stats.score
            sb.prep_high_score()