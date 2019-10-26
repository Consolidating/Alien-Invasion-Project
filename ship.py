#After choosing an image for the ship, we need to display it on the screen. To use our ship, we'll create a new ship module that will contain the class ship.
#This class will manage most of the behaviour of the player ship

import pygame
from pygame.sprite import Sprite #Allows us to get ship to inherit from sprite 

#Pygame is efficient because it allows you to treat all game elements like rectangles(rect) even if they aren't shaped like rectangles

class Ship(Sprite):
	"""A class that manages the ship"""
	def __init__(self,ai_game): #Takes 2 paramters 1) self and 2)reference to the current instance of the AlienInvasion Class. This gives ship access to all the resources in the game 
		"""Initializes the ship and set its starting position"""
		super().__init__()
		
		self.screen = ai_game.screen #assign screen to an attribute of ship  so we can access all attributes of screen 
		self.screen_rect = ai_game.screen.get_rect() #we access screen's rect attribute using get_rect() method and assign it to self.screen_rect 
		#Doing so allows us to place the ship in the correct location on the screen 
		self.settings = ai_game.settings

		#loads the ship image and get its react
		self.image = pygame.transform.scale(pygame.image.load('images/ship.png'),(60,60)) #We call image.load to load images. This function returns a surface representing the ship which we assigned self.image 
		self.rect = self.image.get_rect() #when ship is loaded we use get_rect() to access the ship surface rect attribute so we can later use it to place the ship 

		#Starts each new ship at bottom center of screen
		self.rect.midbottom = self.screen_rect.midbottom #This positions the ship at bottom centre of the screen 

		#Store decimal value for ship horizontal position
		self.x = float(self.rect.x)

		#Movement flags 
		self.moving_right = False #add a flag to ship and set it to false initially. When the moving right is false, ship will be motionless 
		self.moving_left = False 

	def update(self): #Update ships position based on movement flags 
	#update ship's x value and not the rect 
		if self.moving_right and self.rect.right < self.screen_rect.right: #Moves ship if flag is set to True. Code checks the position of the ship before changing value of self.x. self.rect.right returns x coordinates of the right edge of the ship's rect
			self.x += self.settings.ship_speed
		if self.moving_left and self.rect.left > 0:
			self.x -= self.settings.ship_speed
		#Update rect object from self.x
		self.rect.x = self.x 

	def blitme(self): #BlitMe method draws image to the screen at the position specified by self.rect 
		"""Draw the ship at its current location"""
		self.screen.blit(self.image,self.rect)

	def center_ship(self):
		"""Center ship aon the screen"""
		self.rect.midbottom = self.screen_rect.midbottom #sets the rectangle to be same as screen's 
		self.x = float(self.rect.x) #resets x attribute after center 

#rect attributes such as x store only integer values so we need to make modifications to the ship