import pygame
from pygame.sprite import Sprite 

class Alien(Sprite):
	"""A class to represent a single alien in a fleet"""

	def __init__(self,ai_game):
		"""Initialize the alien and set its starting position"""
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings #This allows us to accesss Ai_game attributes

		#Load the alien image and set its rect attribute (In pygame should ALWAYS set RECT attribute))
		self.image = pygame.transform.scale(pygame.image.load('images/alien.png'),(60,48))
		self.rect = self.image.get_rect() #Use get_Rect to get info on image as rectangle 

		#Start each new alien near top left of screen
		self.rect.x = self.rect.width #initially place this on top left of screen since top left is 0,0 
		self.rect.y = self.rect.height #setting the rec attributes height, width = x,y 

		#Store alien's exact horizontal position.
		self.x = float(self.rect.x) #We neeed to track horizontal position since we want to move adjust alien speed 
	
	def update(self):
		"""Move aliens to the right"""
		self.x += (self.settings.alien_speed * self.settings.fleet_direction) #We use self.x to track alien position, fleet direction can be -1 and 1 which repersents left or right depending on if it hits edge 
		self.rect.x = self.x #rectangle x equal to current x 

	def check_edges(self):
		"""Return True if alien is at edge of screen"""
		screen_rect = self.screen.get_rect() #Get rect out of screen
		if self.rect.right >=screen_rect.right or self.rect.left <= 0: #uses the RIGHT attribute of the rectangle to return coordinate for right edge of screen 
			return True
