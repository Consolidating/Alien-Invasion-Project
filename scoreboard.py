import pygame.font #we import pygame.font so it can write text to screen 
from pygame.sprite import Group
from ship import Ship

class Scoreboard:
	"""A class to report scoring information"""
	def __init__(self,ai_game):
		"""Initialize scorekeeping attributes"""
		self.screen = ai_game.screen
		self.screen_rect = self.screen.get_rect()
		self.settings = ai_game.settings
		self.stats = ai_game.stats
		self.ai_game = ai_game


		#Font settings for scoring information
		self.text_color = (255,255,255)
		self.font = pygame.font.SysFont(None,48) #instantiate font object 

		#Prepare initial score image
		self.prep_score() #To turn text to be displayed into image 
		self.prep_high_score() #We will need to create new method since it will be seprate from the score 
		self.prep_level()
		self.prep_ships() 


	def prep_level(self):
		"""Turn the level into a rendered image"""
		level_str = str(self.stats.level)
		self.level_image = self.font.render(level_str,True,self.text_color)

		#Position the level below the score
		self.level_rect = self.level_image.get_rect()
		self.level_rect.right = self.score_rect.right
		self.level_rect.top = self.score_rect.bottom + 10 


	def prep_score(self):
		"""Turn score into rendered image"""
		rounded_score = round(self.stats.score,-1)
		score_str = "{:,}".format(rounded_score) #We turn numerical value stats.score into a string 
		self.score_image = self.font.render(score_str, True, self.text_color) #Pass string to render which creates image 

		#Display score at top right of screen
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20
		self.score_rect.top = 20 

	def prep_high_score(self):
		"""Turn highschore into rendered image"""
		high_score = round(self.stats.high_score,-1) #We round the highscore to nearest 10 and format with commas 
		high_score_str = "{:,}".format(high_score)
		self.high_score_image = self.font.render(high_score_str,True,self.text_color) #we generate image form highscore 

		#Center high score at top of screen
		self.high_score_rect = self.high_score_image.get_rect() #center highscore at top of screen 
		self.high_score_rect.centerx = self.screen_rect.centerx
		self.high_score_rect.top = self.score_rect.top


	def show_score(self):
		"""Draw score to the screen"""
		self.screen.blit(self.score_image,self.score_rect)
		self.screen.blit(self.high_score_image,self.high_score_rect)
		self.screen.blit(self.level_image, self.level_rect)
		self.ships.draw(self.screen)

	def check_high_score(self):
		"""Check to see if there's new high score"""
		if self.stats.score > self.stats.high_score:
			self.stats.high_score = self.stats.score
			self.prep_high_score()

	def prep_ships(self):
		"""Show how many ships are left"""
		self.ships = Group()
		for ship_number in range(self.stats.ships_left):
			ship = Ship(self.ai_game)
			ship.rect.x = 10 + ship_number * ship.rect.width
			ship.rect.y = 10 
			self.ships.add(ship)

		#Prep _ship creates empty group to hold the ship instances. To fill this loop, we run once for every ship the player has left 
		##We set y and x coordinate so they appear next to each other  