# import sys
import pygame
from settings import Settings
from ship import Ship
import game_functions as gf 
from pygame.sprite import Group
# from alien import Alien

def run_game():
    #Initialize the game and create screen object
    pygame.init()
    ai_settings = Settings() #All settings are in this object
    
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    #Make a Ship
    ship = Ship(ai_settings,screen)
    
    # #Make an alien
    # alien = Alien(ai_settings,screen)

    #Make a group to store bullets in.
    bullets = Group()

    #MAke a  group to store aliens in
    aliens = Group()

    #Create a fleet of aliens
    gf.create_fleet(ai_settings,screen,ship,aliens)

    #Start the amin loop for the game
    while True:
        gf.check_events(ai_settings,screen,ship,bullets)
        ship.update()
        gf.update_bullets(ai_settings,screen,ship,aliens,bullets)
        #Here we'll update the alien position after the bullet updation because we'll also need to check for collision.
        gf.update_aliens(ai_settings, aliens)
        gf.update_screen(ai_settings,screen,ship,aliens,bullets)
       
run_game()
