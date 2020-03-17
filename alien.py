import pygame 
from pygame.sprite import Sprite 

class Alien(Sprite):
    """ A class to represent single alien fleet. """
    
    def __init__(self,ai_settings,screen):
        """Initialize the alien and set it's statring position. """
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #Load the alien image and set it's rect attribute
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        #Start each new alien near the top left corner of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #Store a decimal value for the alien exact position
        self.x = float(self.rect.x)

    #Method to draw the image on the postion defined by self.rect
    def blitme(self):
        """ Draw the ship at it's current location """
        self.screen.blit(self.image,self.rect)      

    def update(self):
        """Move the alien right."""
        self.x += self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction
        self.rect.x = self.x

    def check_edges(self):
        """Return True if and alien is at the edge."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
    