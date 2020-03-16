import sys
import pygame
from bullet import Bullet
from alien import Alien

def check_events(ai_settings,screen,ship,bullets):
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

def update_screen(ai_settings,screen,ship,aliens,bullets):
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

    #Make the most recently drawn screen visible.
    pygame.display.flip()


def update_bullets(bullets):
    """Updates position of bullets and get rid of old bullets."""
    #Update bullets position.
    bullets.update()
    #get rid of the bullets that have dissappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    print(len(bullets))

    
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