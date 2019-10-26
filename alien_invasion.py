import sys
import pygame

from settings import Settings #Imports the setting class file we created  
from ship import Ship #Imports ship class 
from bullet import Bullet 
from alien import Alien 
from time import sleep #Used to pause the game when the ship is hit 
from game_stats import GameStats 
from button import Button
from scoreboard import Scoreboard

#The pygame module contains the functionality we need to make a game
#We use tools in sys module to quit when player quits 



class AlienInvasion:
	"""Overall class to manage game assets and behaviour"""

	def __init__(self):
		"""Initialize the game, create the game resource"""
		pygame.init() #Function initializes the background settings that pygame needs to work 
		self.settings = Settings() #Initializes the settings class so we can access its attributes 
		self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height)) #Creates display window to which we will draw game's graphical elements 
		#Background Picture
		self.background_picture = pygame.transform.scale(pygame.image.load(self.settings.background),(self.settings.screen_width,self.settings.screen_height)).convert()

		self.clock = pygame.time.Clock()

		#{FULL SCREEN MODE 
		#self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
		#self.settings.screen_width = self.screen.get_rect().width
		#self.settings.screen_height = self.screen.get_rect().height 
		#}

		#Sets background color
		self.big_color = (230,230,230) #Sets background color to RGB(230,230,230) tuple 

		#We set display tuple to self.screen so it can be accessed throughout class 
		#Object assigned to self.screen is called a surface 
		#Surface in Pygame is part of screen where game element can be displayed 
		#Each element in the game like an alien or ship is its own surface 
		#Surface returned by display.set_mode represents game's entire window 
		#Surface will be redrawn everytime we pass the loop so it can be updated with any changes triggering user input 
		pygame.display.set_caption("Alien Invasion") 

		self.stats = GameStats(self)

		self.ship = Ship(self) #The call to ship() requires one arguement an instance of Alien Invasion
		self.bullets = pygame.sprite.Group() 
		#Self arguement refers to current instance of the game 
		#This gives access to game's resources 

		#Create instance of ALIEN
		self.aliens = pygame.sprite.Group()
		self._create_fleet()
		pygame.mixer.init()
		pygame.mixer.music.load(self.settings.bgm)
		#print(pygame.mixer.music.get_volume())
		pygame.mixer.music.set_volume(pygame.mixer.music.get_volume()+0.5)
		pygame.mixer.music.play(-1)

		self.play_button = Button(self,"Play") #This creates instance with label play but does not draw it onto screen
		self.difficult_button = Button(self,"Difficult")
		self.easy_button = Button(self,"Easy")
		self.sb = Scoreboard(self) #Creates instance of scoreboard 
	def run_game(self): #Game is controlled by run_game method 
		"""Start main game loop"""

		while True:
				self._check_events()


				if self.stats.game_active: #Identifying when parts of game should run 
					self.ship.update()
					self._update_bullets()#Automatically calls update() for each sprite in the group
					self._update_aliens()
				self._update_screen()



	def _check_events(self):
		#Watch for keyboard and mouse events
		for event in pygame.event.get(): #This is an event loop for pygame to recognize events or player actions and respond appropriately 
			#event.get() allows us to access the events that Pygame detects 
			#This function returns list of events that have taken place since this function was last called 
			if event.type == pygame.QUIT:
				#pygame.display.quit()
				sys.exit 
				pygame.quit()
			elif event.type == pygame.KEYDOWN: #In order to allow continuous movement we need KEYUP event 
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)
			elif event.type == pygame.MOUSEBUTTONDOWN: #Pygame detects mousebutton down event when clicked anywhere on screen 
				mouse_pos = pygame.mouse.get_pos() #We want to restrict our game to respond to mouse lcick only on play button. To accomplish this, we use pygame.mouse.get_pos() which returns tuple containing cursor's x and y
				self._check_play_button(mouse_pos) #we send these values to _check_play_button method 
	
	def _check_keydown_events(self,event):

		if event.key == pygame.K_RIGHT: #Helper method 
			self.ship.moving_right = True 
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = True 
		elif event.key == pygame.K_q:
			sys.exit()



		elif event.key == pygame.K_SPACE: 
			self._fire_bullet() #Create new method to fire bullet 
			self.settings.shoot_fx.play()

	def _check_keyup_events(self,event):
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False 

	def _fire_bullet(self):
		"""Creates a new bullet and add it to bullets group"""
		if len(self.bullets) < self.settings.bullets_allowed:
			new_bullet = Bullet(self) #Create new instance of Bullet and call it new_bullet
			self.bullets.add(new_bullet) #We add new_bullet to group of bullets. Add method is same as append but specifically written for pygame Groups 
	def _update_bullets(self):
		"""Updates position of the bullets and get rid of old bullets"""
		self.bullets.update()
			#Get rid of bullets that have dissapeared
		for bullet in self.bullets.copy(): #Have to use copy because Python expects list remain same in original loop. We loop over copy of original list and do the calculations on the copy and then remove the original list one 
			if bullet.rect.bottom <=0: #Check if bullet dissapeared off top screen 
				self.bullets.remove(bullet)
				#print(len(self.bullets)) 
				#debugger used to test if bullet dissapeared
		self._check_bullet_alien_collisions()


	def _check_bullet_alien_collisions(self):
		"""Respond to bullet-alien collision"""
		#Remove any bullets and aliens that collided 
		collisions = pygame.sprite.groupcollide(self.bullets,self.aliens,True, True)
		
		if collisions:
			for aliens in collisions.values():
				self.stats.score += self.settings.alien_points *len(aliens)
			self.sb.prep_score()
			self.sb.check_high_score()

		if not self.aliens:
			#Destroy existing bullets and create new fleet
			self.bullets.empty() #Empty method removes all sprites from group 
			self._create_fleet()
		#sprite.groupcollide() function compares the rects of each element in one group with rects of each element in another group
		#In this case, it compares each bullet rect with each alien rect and return dictionary containing bullets and aliens that have collided
		#Each key in the dictionary will be a bullet and value be the alien hit - This dictionary will be used later on 
		#New code added compares position of all bullets in self.bullets and all aliens in self.aliens and identify any overlaps 
		#The TRUE in collisions tells which sprite to delete 
			self.settings.increase_speed() #Calls increase speed when bullet collides 

			#Increase level
			self.stats.level += 1 #If fleet is desrtyoed, we incrrement value of stats.evel and call pre_levle ot make sure the new level displays correctly  
			self.sb.prep_level()



	def _create_fleet(self):
		"""Creates the fleet of aliens"""
		#make an Alien
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size #Attribute size contains tuple with width and height of rect object 

		#Determine number that can fit screen 
		ship_height = self.ship.rect.height 
		available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height) 
		number_rows = available_space_y//(2*alien_height)
		available_space_x = self.settings.screen_width - (2 * alien_width) #We want 1 alien between each alien so we use 2 alien width to get # aliens + 1 space 
		number_aliens_x = available_space_x // (2*alien_width) #We use double division to get integer 
		

		#Create full fleet of aliens 
		for row_number in range(number_rows): #Counts from 0 to rows we want 
			for alien_number in range(number_aliens_x): #loop max # alien to create aliens 
				self._create_alien(alien_number,row_number)
			

	def _create_alien(self,alien_number,row_number): #Needs alien number thats currently being created 
		"""Create an alien and place it in the row."""
		alien = Alien(self)
		alien_width,height  = alien.rect.size 
		alien.x = alien_width + 2 * alien_width * alien_number #new alien is alien_width + 2 x alien width * number of aliens to push it to the right
		alien.rect.x = alien.x #same rectangle x attribute as class Alien 
		alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
		self.aliens.add(alien) #Adds to fleet which is a sprite group 
	
	def _check_fleet_edges(self): #Loop through the fleet and call check_edges() on each alien from alien.py. if check_edges is TRUE then we call change_fleet_direction 
		"""Respond if alien have reached an edge"""
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break
	
	def _change_fleet_direction(self):
		"""Drop the entire fleet and change the fleet's direction"""
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed #As soon as this is called, we drop the alien y by 1 as it is supposed to change directions AND Drop in alien invaders 
		self.settings.fleet_direction *= -1 #multiplies the direction by -1 to change it 

	
	def _update_aliens(self):
		"""Update position of all aliens in the fleet"""
		self._check_fleet_edges() #Calls check_fleet_edge to constantly check as loop continues
		self.aliens.update() #we use update() method on alien group which calls each alien's update method

		#Check for Alien and Ship Collision
		if pygame.sprite.spritecollideany(self.ship,self.aliens): #spritecollideany() function takes two arguements, a sprite and a group. The function looks for any member of the gorup that has collided with sprite and stop looping through group as soon as it finds one member collided
		#It returns first alien it finds that collided with ship 
			self._ship_hit()
		self._check_aliens_bottom()

	def _update_screen(self):

		
		"""Updates images on the screen and flip to the new screen"""
		#self.screen.fill(self.settings.bg_color) #Fill method acts on a surface. In this case, the surface is screen which is entire display 
		self.screen.blit(self.background_picture,(0,0))
		self.ship.blitme() #draw the ship on the screen so the ship appears on top of the background
		#Make most recently drawn screen visible
		for bullet in self.bullets.sprites(): #bullet.sprites9) method returns a list of all sprites in the group bullets . To draw on screen we loop through the sprite sin bullets and call draw_bullet on each one 
			bullet.draw_bullet()
		self.aliens.draw(self.screen) #makes alien appear on screen 

		#Draw play button if game inactive
		if not self.stats.game_active:
			self.play_button.draw_button()
			self.easy_button.draw_button()
			self.difficult_button.draw_button()
		
		self.sb.show_score()
		pygame.display.flip() #Tells Pygame to make the most recently drawn screen visible #This erases old screen and simply draws a new sceen each time loop is passed 

		
	def _ship_hit(self): #coordinates response when alien hits a ship 
		"""Respond to ship being hit by alien"""
		if self.stats.ships_left > 0:
			#Decrement ships_left
			self.stats.ships_left -= 1 #reduce life (Number of ships) 
			self.sb.prep_ships()
			#Get rid of any remaining aliens and bullets
			self.aliens.empty() #Empty aliens and bullet sprite group 
			self.bullets.empty()
			#Create new fleet and center the ship
			self._create_fleet()
			self.ship.center_ship() #Method to center the ship 
			#Pause
			sleep(0.5) #pause program for half a second 
		else:
			self.stats.game_active = False 
			pygame.mouse.set_visible(True)



	def _check_aliens_bottom(self):
		"""Check if any aliens have reached the bottom of the screen"""
		screen_rect = self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom:
				#Treat this the same as if ship got hit
				self._ship_hit()
				break

	def _check_play_button(self,mouse_pos):
		"""Starts a new game when player click play"""
		play_button_clicked = self.play_button.rect.collidepoint(mouse_pos)
		difficult_button_clicked = self.difficult_button.rect.collidepoint(mouse_pos)
		easy_button_clicked = self.easy_button.rect.collidepoint(mouse_pos)
		
		if play_button_clicked and not self.stats.game_active:
			self._start_game("normal")
		if difficult_button_clicked:
			print("HARD")
			self._start_game("difficult")
		if easy_button_clicked:
			print("EASY")
			self._start_game("easy")

	
	def _start_game(self,mode):
			#Resets game stats
			self.stats.reset_stats() #We reste game stats which gives player three new ships 
			self.sb.prep_score()
			self.sb.prep_level()
			self.sb.prep_ships() #We call it when it is hit so update the display of ship images when player loses a ship 
			self.stats.game_active = True 
			#Hide mouse cursor
			pygame.mouse.set_visible(False) #Passing False to set_visible tells pygame to hide the cursor when mouse is over the game window 
			

		#We use rect method collidepoint() to check whether point of the mouse click overlaps region defined in play butotn rect
		#Get rid of any remaining alien and bullets
			self.aliens.empty() 
			self.bullets.empty()
			#Create new fleet and center ship
			self._create_fleet()
			self.ship.center_ship()
			self.mode = mode 

			#Reset game settings
			self.settings.initialize_dynamic_settings(self.mode)




if __name__ =='__main__':
	#Make game instance and run the game
	ai_game = AlienInvasion()
	ai_game.run_game()






#Helper Method does work inside a class but isn't meant to be called through an instance in Python. Single leading undercore indicates helper method 