import pygame
import sys

pygame.init()


WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((player_x, player_y))
pygame.display.set_caption


WHITE = (255, 255, 255)
RED = (255, 0, 0)


player_size = 50
player_x = WIDTH // 2
player_y = HEIGHT // 2
player_speed = 5


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed

    if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                print('left')
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                print('right')
            if event.key == pygame.K_UP or event.key == ord('w'):
                print('jump')

    if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                print('left stop')
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                print('right stop')
            if event.key == ord('q'):
                pygame.quit()
                sys.exit()
                main = False    

   
    if player_x < 0:
        player_x = 0
    if player_x > WIDTH - player_size:
        player_x = WIDTH - player_size
    if player_y < 0:
        player_y = 0
    if player_y > HEIGHT - player_size:
        player_y = HEIGHT - player_size

    screen.fill(WHITE)
    
    pygame.draw.rect(screen, RED, (player_x, player_y, player_size, player_size))
    
    pygame.display.flip()


    pygame.time.Clock().tick(30)

pygame.quit()
sys.exit()
