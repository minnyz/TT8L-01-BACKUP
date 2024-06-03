import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
WORLD_WIDTH, WORLD_HEIGHT = 1600, 600  # Increased width for horizontal scrolling
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
BACKGROUND_COLOR = (0, 0, 0)

# Load background image
background_image = pygame.image.load("images/background1.png")
background_image = pygame.transform.scale(background_image, (WORLD_WIDTH, WORLD_HEIGHT))

# Load player image
player_image = pygame.image.load("images/maincharacter.png")
player_image = pygame.transform.scale(player_image, (PLAYER_WIDTH, PLAYER_HEIGHT))

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("World(test)")

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT - 100
        self.velocity_y = 0
        self.on_ground = False

    def update(self, platforms):
        # Apply gravity
        self.velocity_y += 0.5

        # Check for player input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = -10
            self.on_ground = False

        # Update vertical position
        self.rect.y += self.velocity_y

        # Boundary checks within the world
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WORLD_WIDTH:
            self.rect.right = WORLD_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity_y = 0
            self.on_ground = True

# Create player
player = Player()

# Sprite groups
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Camera position
camera_x = 0

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update sprites
    all_sprites.update([])

    # Adjust camera position to follow the player
    camera_x = player.rect.x - SCREEN_WIDTH // 2
    camera_x = max(0, min(WORLD_WIDTH - SCREEN_WIDTH, camera_x))

    # Draw background image relative to camera position
    screen.blit(background_image, (-camera_x, 0))

    # Draw everything relative to camera position
    for sprite in all_sprites:
        screen.blit(sprite.image, (sprite.rect.x - camera_x, sprite.rect.y))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()