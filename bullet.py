import pygame
from pygame.sprite import Sprite 

class Bullet(Sprite):
	"""A class to manage bullets fired from the ship"""

	def __init__(self,ai_game): 
		"""Create bullet object at ship's current position"""
		super().__init__() #bullet class inherits from Sprite which we import from pygame.sprite module
		#When you use sprites, you can group related elements in your game and act on all grouped elements at once. To create a bullet instance, __init__() needs current instance of AlienInvasion
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.color = self.settings.bullet_color


		#Create a bullet rect at (0,0) and then set correct position
		self.rect = pygame.Rect(0,0,self.settings.bullet_width, self.settings.bullet_height) #Create bullet's rect attribute. Bullet isn't based on an image so we have to build a rect from scratch using pygame.Rect() class. We initialize the positio nat (0,0)
		#We need to know ship's location 
		self.rect.midtop = ai_game.ship.rect.midtop #We set bullet's midtop attribute to match the ship's 
		#Store bullet position as decimal
		self.y = float(self.rect.y)

	def update(self): #manages the bullet's position. When a bulley is fired, it moves up the screen which corresponds to decreasing y coordinates (since top is 0)
		"""Move the bullet up the screen""" 
		self.y -= self.settings.bullet_speed #we never need to change x coordinate since bullet move only up 
		#Update rect position
		self.rect.y = self.y

	def draw_bullet(self):
		"""Draw bullet to the screen"""
		pygame.draw.rect(self.screen,self.color,self.rect)


