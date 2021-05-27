import pygame
import os
import random

#some defines that will be useful afterwards
Black = (0,0,0)
White = (255,255,255)
Red = (255,0,0)
Green = (0,255,0)
Blue = (0,0,255)
Width = 400
Height = 600
FPS = 60

font_name = pygame.font.match_font("arial")
def draw_text(screen,text,size,x,y):
	font = pygame.font.Font(font_name,size)
	text_surface = font.render(text,True , White)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x,y)
	screen.blit(text_surface,text_rect)

def draw_shield_bar(surf , x, y , pct):
	if pct<0:
		pct = 0
	bar_length = 100
	bar_height = 10
	fill = (pct/150) * bar_length #mesle tanasob gereftan
	fill_rect = pygame.Rect(x,y,fill , bar_height)
	outline_rect = pygame.Rect(x,y,bar_length,bar_height)
	pygame.draw.rect(surf,Green,fill_rect)
	pygame.draw.rect(surf,White,outline_rect,2)	

def darw_lives(surf,img,x,y,lives):
	for i in range(lives):
		img_rect = img.get_rect()
		img_rect.x = x + 30 * i
		img_rect.y = y
		surf.blit(img,img_rect)

def draw_gameover():
	draw_text(screen,"Space Shooter!", 22 , Width/2 , Height/4)
	draw_text(screen,"press SpaceBar to begin",18 , Width/2 , Height/2)
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
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((50,50))
		self.image.fill(Green)
		self.rect = self.image.get_rect()
		self.rect.centerx = Width/2
		self.rect.bottom = Height - 10
		self.speedx = 0

	def update(self):
		self.speedy = 0
		self.speedx = 0 #always zero unless a key is pressed
		keys_pressed = pygame.key.get_pressed() #to handle the keys that user press
		if keys_pressed[pygame.K_RIGHT]:
			self.speedx = 5
		if keys_pressed[pygame.K_LEFT]:
			self.speedx	= -5
		if self.rect.left < 0:
			self.rect.left = 0
		if self.rect.right > Width:
			self.rect.right = Width
		self.rect.x += self.speedx
	def shoot(self):
		bullet = Bullet(self.rect.centerx , self.rect.top)
		all_sprites.add(bullet)
		bullets.add(bullet)

class Enemy(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((40,40))
		self.image.fill(Red)
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(0, Width - self.rect.width)
		self.rect.y = random.randrange(-150 , -100)
		self.speedx = random.randrange(-3,3)
		self.speedy = random.randrange(3,8)

	def update(self):
		self.rect.x += self.speedx
		self.rect.y += self.speedy
		if self.rect.top > Height + 20 or self.rect.right > Width + 50 or self.rect.left < -50:
			self.rect.x = random.randrange(0, Width - self.rect.width)
			self.rect.y = random.randrange(-150 , -100)
			self.speedy = random.randrange(3,8)

class Bullet(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((10,40))
		self.image.fill(White)
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.bottom = y
		self.speedy = -10
	def update(self):
		self.rect.y += self.speedy
		if self.rect.bottom < 0 :
			self.kill() #to delete the ones that move beyond the screen	


#initializing the pygame and the sound system and also the screen
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((Width,Height))
pygame.display.set_caption("Space Shooter!")
Clock = pygame.time.Clock()

score = 0
running = True
game_over = True
#every game has 3 important part : 1)event  2)update  3)draw/render
#game loop:
while running:
#event
	if game_over:
		draw_gameover()
		game_over = False
		#sprites
		all_sprites = pygame.sprite.Group()
		enemys = pygame.sprite.Group()
		bullets = pygame.sprite.Group()
		player = Player()
		all_sprites.add(player)
		for i in range(12):
			enemy = Enemy()
			all_sprites.add(enemy)
			enemys.add(enemy)
		score = 0	

	Clock.tick(FPS)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				player.shoot()


#update
	all_sprites.update()
	#to handle the collides between sprites:
	hits = pygame.sprite.groupcollide(bullets,enemys,True,True) #True means they both disappear
	for hit in hits:
		score += hit.rect.width/2
		enemy = Enemy()
		all_sprites.add(enemy)
		enemys.add(enemy)
	hits = pygame.sprite.spritecollide(player,enemys,False)
	if hits:
		running = False

#draw/render
	screen.fill(Black)
	all_sprites.draw(screen)

	pygame.display.flip()# after EVERYTHING is drawn	

pygame.quit()	
