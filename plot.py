import pygame

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),  pygame.FULLSCREEN)
pygame.display.set_caption("Plot")

Background = pygame.image.load("Assets/Background.png")

intro_font = pygame.font.Font("Assets/cyberpunk_font.ttf", 45)
detail_font = pygame.font.Font("Assets/cyberpunk_font.ttf", 30)

def intro_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def detail_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

run = True
while run:

    screen.fill((255,255,255))

    intro_text("Introduction", intro_font, (0, 0, 0), 50, 50)
    detail_text('In the year 2179, the neon-lit mega-city of Echelon is a bustling \
                metropolis of towering skyscrapers and hidden dangers. Detective Riley Crane, a former corporate \
                security expert turned rogue investigator, is called to investigate the mysterious murder of a high-ranking \
                executive from Orion Industries. The crime scene is a baffling mix of ancient symbols and \
                disabled high-tech security.', detail_font, (0, 0, 0), 50, 150)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False

    pygame.display.flip()

pygame.quit()