#the skeleton of a pygame project
import pygame
import random
#some defines that will be useful afterwards

Width = 360
Height = 480
FPS = 30
White = (255 , 255 ,255)
Black = (0,0,0)
Red =(255 , 0 ,0)
Green = (0 , 255 , 0)
Blue = (0,0,255)

#the first thing to do is to initialize pygame and set up a screen
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((Width,Height))
pygame.display.set_caption("My Game")
Clock = pygame.time.Clock() #for controling FPS

all_sprites = pygame.sprite.Group() #for not getting messy

# now , game loop
# every game has 3 important parts : events , update , draw(render)

running = True

while running:
    Clock.tick(FPS) #to keep the loop at the right speed
    #events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #update
    all_sprites.update()
    
    #draw/render
    screen.fill(Black)
    all_sprites.draw(screen)
    
    pygame.display.flip() # flip after drawing EVERYTHING
    
    
pygame.quit()
