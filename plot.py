import pygame
import time

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Plot")

Background = pygame.image.load("Assets/Background.png")
Background = pygame.transform.scale(Background, (SCREEN_WIDTH, SCREEN_HEIGHT))

intro_font = pygame.font.Font("Assets/cyberpunk_font.ttf", 45)
detail_font = pygame.font.Font("Assets/cyberpunk_2_font.ttf", 30)

# Load the sound effect
letter_sound = pygame.mixer.Sound("Assets/letter_sound.wav")

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

def detail_text(text, font, text_col, x, y, max_width, chars_to_display):
    lines = wrap_text(text, font, max_width)
    total_chars = 0
    for i, line in enumerate(lines):
        if total_chars + len(line) > chars_to_display:
            line = line[:chars_to_display - total_chars]
        img = font.render(line, True, text_col)
        screen.blit(img, (x, y + i * font.get_linesize()))
        total_chars += len(line)
        if total_chars >= chars_to_display:
            break

full_text = ('You are Detective Riley Crane, a top detective in the city of metropolis. You'
            ' are required to take down all of the criminals that are roaming the streets. These'
            ' criminals are armed, so you better be careful. You are free to use excessive force AKA fist/gun. It is'
            ' time to show your skills and save the city.')

chars_displayed = 0
last_update_time = time.time()
char_interval = 0.05  # seconds between each character display

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Draw the background image
    screen.blit(Background, (0, 0))

    # Render the introduction text
    intro_text("Introduction", intro_font, (0, 0, 255), 50, 50)
    
    # Render the detailed plot text with wrapping, displaying only the current number of characters
    detail_text(full_text, detail_font, (255, 0, 255), 50, 150, SCREEN_WIDTH - 100, chars_displayed)
    
    # Update the number of characters displayed based on the time elapsed
    current_time = time.time()
    if chars_displayed < len(full_text) and current_time - last_update_time > char_interval:
        chars_displayed += 1
        letter_sound.play()
        last_update_time = current_time

    pygame.display.flip()

pygame.quit()
