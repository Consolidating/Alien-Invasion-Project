import pygame.font #Pygame Font module lets pygame render text to the screen 

class Button:
	def __init__(self,ai_game,msg): #Init takes parameter self, the ai_game object and msg which contains text of button
		"""Initialize button attributes"""
		self.screen = ai_game.screen
		self.screen_rect = self.screen.get_rect()

		#Set dimensons and properties of the button
		self.width, self.height = 200,50 #We set the demensions of the button 
		self.text_color = (255,255,255)
		self.font = pygame.font.SysFont(None,48) #Prepare a font attribute for rendering text.
		#Non arguement tells pygame to use default font nad 48 specifies the size of text 

		#Build button's rect object and center it
		self.rect = pygame.Rect(0,0,self.width,self.height) #we create rect for butotn and set its center attribute to match that of screen
		if msg == "Play":
			self.rect.center = self.screen_rect.center
			self.button_color = (0,255,0)
		if msg == "Difficult":
			self.rect.center = (100,500)
			self.button_color = (255,0,0)
		if msg == "Easy":
			self.rect.center = (100,550)
			self.button_color = (255,0,0)
	

		#Button message needs to be prepared only once

		#Pygame works with text by rendering the string you want to display as an image
		#We call _prep_msg() to handle this rendering 
		self._prep_msg(msg) 

	def _prep_msg(self,msg):
		"""Turn msg into rendered image and center text on button"""
		self.msg_image = self.font.render(msg,True,self.text_color, self.button_color) #font.render turns text stored in msg into image which we then store as self.msg_image. 
		#font.render() method also takes boolean value to turn antialiasing on or off - antialiasing makes edges of text smoother. If you do not include background color pygame will render transparent 
		self.msg_image_rect = self.msg_image.get_rect() 
		self.msg_image_rect.center = self.rect.center #We set center of button to center of screen attribute 

	def draw_button(self):
		#Draw blank button and then draw message
		self.screen.fill(self.button_color,self.rect) #we use fill to draw rectangle portion of button
		self.screen.blit(self.msg_image, self.msg_image_rect)  #We call blit to draw text image to screen passing it to an image and rect object associated with the image 
 
