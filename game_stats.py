#GameStats to track score 
#We make one GameStats instance for the entire duration Alien Invasion is running 
#We need to reset stats each time player starts new game 
class GameStats:
	"""Tracks statistics for Alien Invasion"""
	def __init__(self,ai_game):
		"""Initializes statistics"""
		self.settings = ai_game.settings
		self.reset_stats()
		#Start Alien Invasion in inactive state
		self.game_active = False 
		self.high_score = 0 #Tracks highscore. We initialize the high score in __init__ rather than reset_stats as it should be never be reset


	def reset_stats(self): #Resets 
		"""Initializes statistics that can change during game"""
		self.ships_left = self.settings.ship_limit #This is value of health or ships lefts
		self.score = 0 
		self.level = 1 

