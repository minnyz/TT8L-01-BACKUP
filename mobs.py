import pygame
import spritesheet

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Spritesheets')

sprite_sheet_image = pygame.image.load('assets/mobsLow/1/Idle.png').convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)

BG = (50, 50, 50)
BLACK = (0, 0, 0)

# Animation
animation_list = []
animation_steps = 4
last_update = pygame.time.get_ticks()
animation_cooldown = 100
frame = 0
for x in range(animation_steps):
    animation_list.append(sprite_sheet.get_image(x, 48, 48, 3, BLACK))

# Movement parameters
movement_radius = 200  # Adjust as needed
movement_speed = 2  # Adjust as needed
direction = 1  # 1 for right, -1 for left
position = SCREEN_WIDTH // 2  # Starting position

run = True
clock = pygame.time.Clock()

while run:
    screen.fill(BG)

    # Update animation
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:
        frame += 1
        last_update = current_time
        if frame >= len(animation_list):
            frame = 0

    # Update position
    position += movement_speed * direction

    # Check boundaries
    if position >= SCREEN_WIDTH - movement_radius:
        direction = -1
    elif position <= movement_radius:
        direction = 1

    # Blit animation frame at the current position
    screen.blit(animation_list[frame], (position - animation_list[frame].get_width() // 2, SCREEN_HEIGHT // 2 - animation_list[frame].get_height() // 2))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()
