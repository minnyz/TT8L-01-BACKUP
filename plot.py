import pygame

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Plot")

Background = pygame.image.load("Assets/Background.png")
Background = pygame.transform.scale(Background, (SCREEN_WIDTH, SCREEN_HEIGHT))

intro_font = pygame.font.Font("Assets/cyberpunk_font.ttf", 45)
detail_font = pygame.font.Font("Assets/cyberpunk_2_font.ttf", 30)

def intro_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def wrap_text(text, font, max_width):
    lines = []
    words = text.split(' ')
    while words:
        line = ''
        while words and font.size(line + words[0])[0] <= max_width:
            line += (words.pop(0) + ' ')
        lines.append(line)
    return lines

def detail_text(text, font, text_col, x, y, max_width):
    lines = wrap_text(text, font, max_width)
    for i, line in enumerate(lines):
        img = font.render(line, True, text_col)
        screen.blit(img, (x, y + i * font.get_linesize()))

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Draw the background image
    screen.blit(Background, (0, 0))

    # Render the introduction text
    intro_text("Introduction", intro_font, (0, 0, 255), 50, 50)
    
    # Render the detailed plot text with wrapping
    detail_text('In the year 2179, the neon-lit mega-city of Echelon is a bustling '
                'metropolis of towering skyscrapers and hidden dangers. Detective Riley Crane, a former corporate '
                'security expert turned rogue investigator, is called to investigate the mysterious murder of a high-ranking '
                'executive from Orion Industries. The crime scene is a baffling mix of ancient symbols and '
                'disabled high-tech security.'
                'As Crane delves into the case, he uncovers whispers of an underground movement called "The Veil," '
                "rumored to be fighting against corporate corruption. Navigating through Echelon's dangerous streets, "
                'Crane must gather clues, interrogate suspects, and make critical decisions that will shape the outcome of his investigation.'
                "tep into Crane's shoes and uncover the secrets of "
                '"Neon Veil." ' 
                "Explore the city's dark underbelly, solve the mystery, and decide the fate of Echelon."
                'Welcome to a world where nothing is as it seems. ', detail_font, (255, 0, 255), 50, 150, SCREEN_WIDTH - 100)

    pygame.display.flip()

pygame.quit()
