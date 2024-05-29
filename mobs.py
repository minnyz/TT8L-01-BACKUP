import pygame
import spritesheet

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Spritesheets')

sprite_sheet_image = pygame.image.load('assets/mobsLow/1/Idle.png').convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)

BG =(50, 50, 50)
BLACK = (0, 0, 0)

frame_0 = sprite_sheet.get_image( 0, 48, 48, 3, BLACK)
frame_1 = sprite_sheet.get_image( 1, 48, 48, 3, BLACK)
frame_2 = sprite_sheet.get_image( 2, 48, 48, 3, BLACK)
frame_3 = sprite_sheet.get_image( 3, 48, 48, 3, BLACK)

run = True
while run:
    
    #background
    screen.fill(BG)
    
    #display npc
    screen.blit(frame_0, (0,0))
    screen.blit(frame_1, (130,0))
    screen.blit(frame_2, (260,0))
    screen.blit(frame_3, (390,0))
    
    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
            
    pygame.display.update()
pygame.quit()







