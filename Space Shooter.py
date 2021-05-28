#Ramtin Ehsani
#ID = 97521018
#Final Project(Pygame)
#Space Shooter game
import pygame
import random
import os

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder,"Images")
audio_folder = os.path.join(game_folder,"Audio")
anime_folder = os.path.join(game_folder,"Explosions")
anime_folder2 = os.path.join(game_folder,"player_expl")

#some defines that will be useful afterwards

Width = 480
Height = 600
FPS = 60
White = (255,255,255)
Black = (0,0,0)
Red =(255,0,0)
Green = (0,255,0)
Blue = (0,0,255)

font_name = pygame.font.match_font("arial")
def draw_text(surf , text ,size, x, y):
	font = pygame.font.Font(font_name,size)
	text_surface = font.render(text , True , White) #true is for anti-aliass
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x,y)
	surf.blit(text_surface,text_rect)

def draw_shield_bar(surf , x, y , pct):
	if pct<0:
		pct = 0
	bar_length = 100
	bar_height = 10
	fill = (pct/150) * bar_length #mesle tanasob gereftan
	fill_rect = pygame.Rect(x,y,fill , bar_height)
	pygame.draw.rect(surf,Green,fill_rect)

def darw_lives(surf,img,x,y,lives):
	for i in range(lives):
		img_rect = img.get_rect()
		img_rect.x = x + 30 * i
		img_rect.y = y
		surf.blit(img,img_rect)

def draw_gameover():
	screen.blit(background2,background2_rect)
	draw_text(screen,"Space Shooter!", 22 , Width/2 , Height/4)
	draw_text(screen,"Project", 20 , Width/2 , Height/3)
	draw_text(screen,"press SpaceBar to begin",18 , Width/2 , Height/2)
	draw_text(screen,"High Score:",20,Width/2 , Height/3 + 40)
	draw_text(screen,str(max(high_score)),20, Width/2 + 70 ,Height/3 + 40)
	pygame.display.flip()
	waiting = True
	while waiting:
		Clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					waiting = False	

class Player(pygame.sprite.Sprite):
	'''for creating the space ship'''
	def __init__(self):
		pygame.sprite.Sprite.__init__(self) #without this call sprite wont work
		self.image = pygame.transform.scale(pygame.image.load(os.path.join(img_folder,"playerShip.png")).convert(),(62,40))
		self.radius = 25
		self.image.set_colorkey(Black)
		self.rect = self.image.get_rect()
		#pygame.draw.circle(self.image, Red ,self.rect.center,self.radius )
		self.rect.centerx = Width/2
		self.rect.bottom = Height - 10
		self.speedx = 0
		self.shield = 150
		self.lives = 3
		self.hidden = False
		self.hidden_timer = pygame.time.get_ticks()
		

	def update(self):
		#unhide if hidden
		if self.hidden and pygame.time.get_ticks() - self.hidden_timer > 1500:
			self.hidden = False
			self.rect.centerx = Width/2
			self.rect.bottom = Height - 10 
		self.speedx = 0 #always zero unless a key is pressed
		self.speedy = 0
		keys_pressed = pygame.key.get_pressed() # a list of keys getting pressed
		
		if keys_pressed[pygame.K_RIGHT]:
			self.speedx = 5
		if keys_pressed[pygame.K_LEFT]:
			self.speedx = -5
		if self.rect.left < 0 :
			self.rect.left = 0     #now the edges works like walls
		if self.rect.right > Width :
			self.rect.right =  Width    
	   
		self.rect.x += self.speedx
	def shoot(self):
		bullet = Bullets(self.rect.centerx, self.rect.top) #bottom of the bullet at the top of the player
		all_sprites.add(bullet)
		bullets.add(bullet) 
		shoot_sound.play()   
	def hide(self):
		self.hidden_timer = pygame.time.get_ticks()
		self.rect.centerx = Width/2
		self.rect.bottom = Height + 200
		self.hidden = True
		
class Enemy(pygame.sprite.Sprite):
	'''for creating meteors'''
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(random.choice(meteor_images)).convert()
		self.image.set_colorkey(Black)
		self.rect = self.image.get_rect()
		self.radius = int(self.rect.width*0.9 /2)
		#pygame.draw.circle(self.image, Red ,self.rect.center,self.radius )       
		self.rect.x = random.randrange(0, Width - self.rect.width) # isurance that it will be appeared somwhere between the widht
		self.rect.y = random.randrange(-150,-100)
		self.speedy = random.randrange(3,8)
		self.speedx = random.randrange(-3,3)

	def update(self):
		self.rect.y += self.speedy
		self.rect.x += self.speedx
		if self.rect.top > Height + 20 or self.rect.left< -90 or self.rect.right> Width+90 : #to send the Enemy randomly up when it reaches the bottom
			self.rect.x = random.randrange(0, Width - self.rect.width)
			self.rect.y = random.randrange(-100,-40)
			self.speedy = random.randrange(4,8)

class Bullets(pygame.sprite.Sprite):
	'''for creating laser shots'''
	def __init__(self , x ,y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(pygame.image.load(os.path.join(img_folder,"laser.png")).convert(),(8,40))
		self.image.set_colorkey(Black)
		self.rect = self.image.get_rect()
		self.rect.bottom = y
		self.rect.centerx = x
		self.speedy = -10 #so that it moves up

	def update(self):
		self.rect.y += self.speedy
		# to delete the bullet that moves off the top of the screen
		if self.rect.bottom < 0 :
			self.kill()    

class Explosion(pygame.sprite.Sprite):
	'''for creating explosions'''
	def __init__(self,center,size):
		pygame.sprite.Sprite.__init__(self)
		self.size = size
		self.image = explosion_anime[self.size][0]
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.frame = 0
		self.last_update = pygame.time.get_ticks()
		self.frame_rate = 50
	def update(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > self.frame_rate:
			self.last_update = now
			self.frame += 1
			if self.frame == len(explosion_anime[self.size]):
				self.kill()
			else:
				center = self.rect.center
				self.image = explosion_anime[self.size][self.frame]
				self.rect = self.image.get_rect()
				self.rect.center = center		


#the first thing to do is to initialize pygame and set up a screen
pygame.init()
pygame.mixer.init() #initializing sound
screen = pygame.display.set_mode((Width,Height))
pygame.display.set_caption("Space Shooter!")
Clock = pygame.time.Clock() #for controling FPS

#Load all game graphics
background = pygame.image.load(os.path.join(img_folder,"Space Shooter Background.png"))
background_rect = background.get_rect()
background2 = pygame.image.load(os.path.join(img_folder,"Space Shooter Background2.png"))
background2_rect = background2.get_rect()

meteor_list = ["meteorBrown_big1.png","meteorBrown_med1.png" , "meteorBrown_tiny1.png",
			   "meteorBrown_small1.png"]
meteor_images = []
for img in meteor_list:
	meteor_images.append(os.path.join(img_folder,img))

explosion_anime = {}
explosion_anime["small"]= []
explosion_anime["large"]= []
explosion_anime["player"]= []
for i in range(8):
	file_name = "regularExplosion0{}.png".format(i)
	img = pygame.image.load(os.path.join(anime_folder,file_name)).convert()
	img.set_colorkey(Black)
	img_small = pygame.transform.scale(img,(32,32))
	img_large = pygame.transform.scale(img,(75,75))
	explosion_anime["small"].append(img_small)
	explosion_anime["large"].append(img_large)
	file_name = "sonicExplosion0{}.png".format(i)
	img = pygame.image.load(os.path.join(anime_folder2,file_name))
	img.set_colorkey(Black)
	explosion_anime["player"].append(img)

#Load sounds
explosion_list=["Explosion1","Explosion2"]
explosion_sound = []
for exp in explosion_list:
	explosion_sound.append(pygame.mixer.Sound(os.path.join(audio_folder,exp)))
shoot_sound = pygame.mixer.Sound(os.path.join(audio_folder,"Laser_Shoot"))
pygame.mixer.music.load(os.path.join(audio_folder,"SkyFire.ogg"))
pygame.mixer.music.set_volume(0.3)

	


lives_img = pygame.transform.scale(pygame.image.load(os.path.join(img_folder,"playerShip.png")).convert(),(25,19))
lives_img.set_colorkey(Black)

pygame.mixer.music.play(loops=-1) #-1 means that when it ends, it starts from the begining

running = True
game_over = True
high_score = [0]
# now , game loop
# every game has 3 important parts : events , update , draw(render)
while running:
	if game_over:
		draw_gameover()
		game_over = False
		all_sprites = pygame.sprite.Group() #for not getting messy
		enemys = pygame.sprite.Group()
		bullets = pygame.sprite.Group()
		player = Player()
		all_sprites.add(player)
		for i in range(14):
			enemy = Enemy()
			all_sprites.add(enemy)
			enemys.add(enemy)
		score = 0	
	Clock.tick(FPS) #to keep the loop at the right speed
#events
	for event in pygame.event.get():
		if event.type == pygame.QUIT: #for closing the window
			running = False
		elif event.type == pygame.KEYDOWN :  #for shooting
			if event.key == pygame.K_SPACE:
				player.shoot()  


#update
	all_sprites.update()


	#to control what happens when Enemys hit the player
	hits = pygame.sprite.spritecollide(player,enemys,True, pygame.sprite.collide_circle) #a list of Enemys hitting the player
	#by default , collision is based on rectangles . so we can change it
	for hit in hits:
		m = Enemy()
		all_sprites.add(m)
		enemys.add(m)
		player.shield -= hit.radius *2
		expl = Explosion(hit.rect.center,"small")
		random.choice(explosion_sound).play()
		all_sprites.add(expl)

		
		if player.shield <= 0:
			death = Explosion(hit.rect.center,"player")
			all_sprites.add(death)
			player.hide()
			player.lives -= 1
			player.shield = 150

	if player.lives == 0 and not death.alive():
		game_over= True

	#to control what happens when bullets hit the Enemys
	hits = pygame.sprite.groupcollide(enemys,bullets,True,True) #true means it will disappear after the collide and we need both to remove
	#but what happens is that when we shoot them, they will never come back . to avoid that :
	for hit in hits :
		m = Enemy()
		all_sprites.add(m)
		enemys.add(m)
		score += 55 - hit.radius
		expl = Explosion(hit.rect.center,"large")
		all_sprites.add(expl)
		random.choice(explosion_sound).play()
		high_score.append(score)


#draw/render
	screen.fill(Black)
	screen.blit(background,background_rect) #for background graphics
	all_sprites.draw(screen)
	draw_text(screen,str(score),20 , Width/2 , 10)	
	draw_shield_bar(screen,15 , 15 , player.shield)
	darw_lives(screen,lives_img, Width - 100 , 5 , player.lives)
	pygame.display.flip() # after EVERYTHING is drawn
		
pygame.quit()