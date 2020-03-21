class Settings():
    """ A class to store all the settings for our Alien Invasion Game. """

    def __init__(self):
        """ Initialize the game's settings """

        #Screen settings
        #Height and Width of our game screen.
        self.screen_width = 1200
        self.screen_height = 800

        #Set the background color of the window
        self.bg_color = (230,230,230)

        #Ship Settings
        # self.ship_speed_factor = 1.5
        self.ship_limit = 3

        #Bullet Settings(small rectangle)
        # self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3

        #Alien Settings
        # self.alien_speed_factor = 0.5
        self.fleet_drop_speed = 10
        # #fleets direction of 1 represents right and -1 represents left.
        # self.fleet_direction = 1

        #How quickly the game speeds up
        self.speedup_scale = 1

        #How quickly the alien point score scale increase
        self.score_scale = 1.5

        self.initialize_dyanamic_settings()

    def initialize_dyanamic_settings(self):
        """Initialize settings that change throughout the game"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        #fleets direction of 1 represents right and -1 represents left.
        self.fleet_direction = 1    
        
        #Scoring
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings and alien points value"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)