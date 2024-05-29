import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
WORLD_WIDTH, WORLD_HEIGHT = 1600, 600  # Increased width for horizontal scrolling
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
PLAYER_COLOR = (0, 0, 255)
PLATFORM_COLOR = (255, 255, 255)
BACKGROUND_COLOR = (0, 0, 0)

# Load background image
background_image = pygame.image.load("images/background1.png")  # Replace "your_background_image.jpg" with your image file
background_image = pygame.transform.scale(background_image, (WORLD_WIDTH, WORLD_HEIGHT))

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("World(test)")

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(PLAYER_COLOR)
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

        # Check for collisions with platforms
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                # Check if falling
                if self.velocity_y > 0 and self.rect.bottom > platform.rect.top:
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True

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

# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(PLATFORM_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Create player
player = Player()

# Create platforms
platforms = pygame.sprite.Group()
platforms.add(Platform(0, SCREEN_HEIGHT - 50, WORLD_WIDTH, 50))
platforms.add(Platform(200, 400, 200, 20))
platforms.add(Platform(450, 300, 200, 20))
platforms.add(Platform(700, 200, 200, 20))
platforms.add(Platform(1000, 400, 200, 20))
platforms.add(Platform(1300, 300, 200, 20))

# Sprite groups
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(*platforms)

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
    all_sprites.update(platforms)

    # Adjust camera position to follow the player
    camera_x = player.rect.x - SCREEN_WIDTH // 2
    camera_x = max(0, min(WORLD_WIDTH - SCREEN_WIDTH, camera_x))

    # Draw background image
    screen.blit(background_image, (0, 0))

    # Draw everything
    for sprite in all_sprites:
        screen.blit(sprite.image, (sprite.rect.x - camera_x, sprite.rect.y))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()