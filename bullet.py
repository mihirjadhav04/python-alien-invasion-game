import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """ A Class to handle bullets fired from the ship."""

    def __init__(self,ai_settings,screen,ship):
        """Create a bullet object at the ships current position. """
        super().__init__()
        self.screen = screen

        #Create a bullet rect at (0,0) and then set it's correct position
        self.rect = pygame.Rect(0,0,ai_settings.bullet_width,ai_settings.bullet_height) #As bullet is not the image we need to create it from scratch using Rect()
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        #Store the bullet position as a decimal value
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """Move the bullet up the screen"""
        #Update the decimal position of the bullet
        self.y -= self.speed_factor
        #Update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen"""
        pygame.draw.rect(self.screen,self.color,self.rect)


