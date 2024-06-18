import pygame
import sys

def main():
    pygame.init()

    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Plot")

    Background = pygame.image.load("Assets/Background.png")
    Background = pygame.transform.scale(Background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    intro_font = pygame.font.Font("Assets/cyberpunk_font.ttf", 45)
    detail_font = pygame.font.Font("Assets/cyberpunk_2_font.ttf", 20)

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

    def draw_button(text, font, text_col, button_col, x, y, width, height):
        pygame.draw.rect(screen, button_col, (x, y, width, height))
        text_surf = font.render(text, True, text_col)
        text_rect = text_surf.get_rect(center=(x + width / 2, y + height / 2))
        screen.blit(text_surf, text_rect)
        return pygame.Rect(x, y, width, height)

    def show_intro():
        screen.blit(Background, (0, 0))
        intro_text("Introduction", intro_font, (0, 0, 255), 50, 50)
        detail_text(
            'In the year 2179, the neon-lit mega-city of Echelon is a bustling '
            'metropolis of towering skyscrapers and hidden dangers. Detective Riley Crane, a former corporate '
            'security expert turned rogue investigator, is called to investigate the mysterious murder of a high-ranking '
            'executive from Orion Industries. The crime scene is a baffling mix of ancient symbols and '
            'disabled high-tech security.'
            'As Crane delves into the case, he uncovers whispers of an underground movement called "The Veil," '
            "rumored to be fighting against corporate corruption. Navigating through Echelon's dangerous streets, "
            'Crane must gather clues, interrogate suspects, and make critical decisions that will shape the outcome of his investigation.'
            "Step into Crane's shoes and uncover the secrets of "
            '"Neon Veil." ' 
            "Explore the city's dark underbelly, solve the mystery, and decide the fate of Echelon."
            'Welcome to a world where nothing is as it seems. ', detail_font, (255, 0, 255), 50, 150, SCREEN_WIDTH - 100
        )
        button_rect = draw_button("Continue", intro_font, (255, 255, 255), (0, 128, 0), SCREEN_WIDTH - 200, SCREEN_HEIGHT - 100, 150, 50)
        return button_rect

    run = True
    show_intro_page = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if show_intro_page and continue_button_rect.collidepoint(mouse_pos):
                    show_intro_page = False

        if show_intro_page:
            continue_button_rect = show_intro()
        else:
            import chapter
            chapter.main()

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
