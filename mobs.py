import pygame
import random
import math


pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Drone NPC Movement")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()

class DroneNPC(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/mobsLow/1/Idle.png").convert_alpha()
        self.image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        
        self.speed = 2
        self.angle = 0
        self.angular_speed = 0.05

    def update(self):
        self.image = pygame.transform.rotate(self.image, pygame.time.get_ticks() / 10 * self.angular_speed)
        self.rect = self.image.get_rect(center=self.rect.center)
        
        self.image = pygame.transform.rotate(self.image, math.degrees(-self.angle))
        
        
        if self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0
        elif self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.bottom = 0
        elif self.rect.bottom < 0:
            self.rect.top = SCREEN_HEIGHT

all_sprites = pygame.sprite.Group()
drone = DroneNPC()
all_sprites.add(drone)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update all sprites
    all_sprites.update()
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()







