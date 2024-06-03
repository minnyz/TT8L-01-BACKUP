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
background_image = pygame.image.load("images/background1.png")  # Replace with your image file
background_image = pygame.transform.scale(background_image, (WORLD_WIDTH, WORLD_HEIGHT))

# Load character sprite sheet
sprite_sheet = pygame.image.load("mc/mc_idle.png")  # Replace with your sprite sheet image

# Define the dimensions of each frame in the sprite sheet
FRAME_WIDTH, FRAME_HEIGHT = 50, 50  # Adjust according to your sprite sheet

# Function to extract individual frames from the sprite sheet
def extract_frames(sheet, frame_width, frame_height, row):
    frames = []
    sheet_width, sheet_height = sheet.get_size()
    for x in range(0, sheet_width, frame_width):
        frame = sheet.subsurface((x, row * frame_height, frame_width, frame_height))
        frame = pygame.transform.scale(frame, (PLAYER_WIDTH, PLAYER_HEIGHT))
        frames.append(frame)
    return frames

# Extract idle frames from the sprite sheet (assuming they are on row 0)
idle_frames = extract_frames(sprite_sheet, FRAME_WIDTH, FRAME_HEIGHT, row=0)

# Extract running frames from the sprite sheet (assuming they are on row 1)
running_frames = extract_frames(sprite_sheet, FRAME_WIDTH, FRAME_HEIGHT, row=1)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("World(test)")

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.idle_frames = idle_frames
        self.running_frames = running_frames
        self.current_frame = 0
        self.image = self.idle_frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT - 100
        self.velocity_y = 0
        self.on_ground = False
        self.animation_timer = 0
        self.animation_speed = 10  # Adjust this for faster/slower animation
        self.is_running = False

    def update(self, platforms):
        # Apply gravity
        self.velocity_y += 0.5

        # Check for player input
        keys = pygame.key.get_pressed()
        self.is_running = False
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
            self.is_running = True
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
            self.is_running = True
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

        # Update animation frame
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.idle_frames if not self.is_running else self.running_frames)
            self.image = (self.idle_frames if not self.is_running else self.running_frames)[self.current_frame]

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
    all_sprites.update([])  # No platforms

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