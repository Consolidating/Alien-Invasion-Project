import pygame

class Settings:
	"""A class to store all settings for Alien Invasion"""

	def __init__(self):
		"""Initialize the game's static settings"""
		#Screen Settings
		self.screen_width = 1200
		self.screen_height = 600
		self.bg_color = (230,230,230)


		#Bullet Settings
		self.bullet_width = 5
		self.bullet_height = 15 
		self.bullet_color = (255,255,255) 
		self.bullets_allowed = 3 #limits the bullets 

		#Alien Settings
		self.fleet_drop_speed = 10 
		self.fleet_direction = 1 #1 represents right while -1 represents left 


		#Music 
		self.bgm = r'bgm\02.mp3'
		self.shoot_fx = pygame.mixer.Sound(r'bgm\shoot.wav')
		self.shoot_fx.set_volume(self.shoot_fx.get_volume()-0.5)



		#Ship setting
		self.ship_limit = 3 

		#How quickly the game speeds up
		self.speedup_scale = 1.1 #Add speedup_scale setting to control how quickly the game speeds up 
		#self.initialize_dynamic_settings() #We call initialize_dynamic_settings() method to initialize the values for attributes that need to change throughout game 


		#Pictures
		#self.background = r'images\space.jpg'
		self.background = r'images\bg.png'

	def initialize_dynamic_settings(self,mode):
		"""Initialize dynamic settings that change throughout game"""
		if mode =="easy":
			self.mode_multi = 0.5
		if mode =="difficult":
			self.mode_multi = 10
		else:
			self.mode_multi = 1 

		self.ship_speed = 1.5
		self.bullet_speed = 2.0
		self.alien_speed = 1  * self.mode_multi

		#Scoring
		self.alien_points = 1000
		self.score_scale = 1.5 


		#fleet_direction of 1 repreesnts right; -1 represent left
		self.fleet_direction = 1 #We use this so aliens always move right at beginning of the game 
		#We don't increase value of fleet_drop_speed becauase as aliens move right faster they will move down faster 
	def increase_speed(self): #Increaes the speed of the ships, bullets and aliens each time the player reaches a new level
		"""Increase speed setting"""
		self.ship_speed *= self.speedup_scale
		self.bullet_speed *= self.speedup_scale
		self.alien_speed *= self.speedup_scale
		self.alien_points = int(self.alien_points*self.score_scale)
		#We multiply each speed setting by value of speed_ups scale 
	
	def difficulty(self,multi):
		"""Sets difficulty of game"""
		self.multi = multi
		self.alien_speed = self.alien_speed * multi

