import pygame

class Ship():

    #The __init__() method of Ship takes two parameters: the self reference and the screen where we’ll draw the ship.
    def __init__(self,ai_settings,screen):
        """ Initialize the ship and set it's starting position """
        self.screen = screen
        #Added ai_settings so that ship has acces to the speed_factor attribute.
        self.ai_settings = ai_settings

        #Load the ship image and  get it's rect.
        self.image = pygame.image.load('images/ship.bmp')#pygame.image.load() - to load the image,returns surface representing the ship.
        self.rect = self.image.get_rect() # to access surface rect attribute. (rect object)
        self.screen_rect = screen.get_rect() 

        """
        When working with a rect object, you can use the x- and y-coordinates
        of the top, bottom, left, and right edges of the rectangle, as well as the
        center. You can set any of these values to determine the current position
        of the rect.
        """    

        #Start each new ship at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        #Store a decimal value for the ship center
        self.center = float(self.rect.centerx)

        #Movement Flag - for ship moment
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """ Update the ship's position based on the movement of the flag."""
        if self.moving_right and self.rect.right < self.screen_rect.right :
            #update the ship center value ,not rect. Because rect will take only the integer part and not decimal. So to store accurately we'll use center.
            self.center += self.ai_settings.ship_speed_factor

        if self.moving_left and self.rect.left > 0 :
            self.center -= self.ai_settings.ship_speed_factor

        #Update the rect object from center.
        self.rect.centerx = self.center

    #Method to draw the image on the postion defined by self.rect
    def blitme(self):
        """ Draw the ship at it's current location """
        self.screen.blit(self.image,self.rect)
