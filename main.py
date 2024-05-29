import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
WORLD_WIDTH, WORLD_HEIGHT = 1600, 600  # Increased width for horizontal scrolling
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
PLAYER_COLOR = (0, 0, 255)
PLATFORM_COLOR = (0, 255, 0)
BACKGROUND_COLOR = (0, 0, 0)

# Load background image
background_image = pygame.image.load("background1.jpg")  # Replace "your_background_image.jpg" with your image file
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