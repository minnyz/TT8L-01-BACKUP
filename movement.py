import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Player Movement')

WHITE = (255, 255, 255)
RED = (255, 0, 0)

player_size = 75
player_x = 10
player_y = HEIGHT - player_size  
player_speed = 5

is_jumping = False
jump_speed = 10
gravity = 0.5
player_velocity_y = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                print('left')
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                print('right')
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                print('down')
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                if not is_jumping:
                    is_jumping = True
                    player_velocity_y = -jump_speed
                    print('jump')
            if event.key == ord('q'):
                pygame.quit()
                sys.exit()
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                print('left stop')
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                print('right stop')

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed

    if is_jumping:
        player_y += player_velocity_y
        player_velocity_y += gravity
        if player_y >= HEIGHT - player_size:
            player_y = HEIGHT - player_size
            is_jumping = False
            player_velocity_y = 0

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

    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
