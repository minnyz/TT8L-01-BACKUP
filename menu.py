import pygame, sys
from button import Button


pygame.init()

# Loud the click sound
pygame.mixer.init()
click_sound =  pygame.mixer.Sound("assets/enterface_click_2.mp3")

# Create the screen and set the title
SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

# for background
BG = pygame.image.load("assets/Background.png")

def get_font_1(size): 
    return pygame.font.Font("assets/cyb3.ttf", size)

def get_font_2(size):
    return pygame.font.Font("assets/cyb_options.otf", size)

def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(BG, (0, 0))

        PLAY_TEXT = get_font_1(45).render("PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font_1(75), base_color="White", hovering_color="Red")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    click_sound.play()
                    main_menu()

        pygame.display.update()
    
def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(BG,(0, 0))

        OPTIONS_TEXT = get_font_1(100).render("OPTIONS", True, "#b68f40")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 60))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
        
        AUDIO_BUTTON = Button(image=None, pos=(180, 200),
                            text_input="Audio", font=get_font_1(75), base_color="White", hovering_color="Yellow")
                
        VIDEO_BUTTON = Button(image=None, pos=(180, 300),
                              text_input="Video", font=get_font_1(75), base_color="White", hovering_color="Yellow")
    
        KEY_BUTTON = Button(image=None, pos=(318, 400),
                            text_input="Key Bindings", font=get_font_1(75), base_color="White", hovering_color="Yellow")   

        OPTIONS_BACK = Button(image=None, pos=(180, 500), 
                            text_input="Back", font=get_font_1(75), base_color="White", hovering_color="Red")
        
        for button in [AUDIO_BUTTON, OPTIONS_BACK, VIDEO_BUTTON, KEY_BUTTON]:    
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    click_sound.play()
                    main_menu()
                if AUDIO_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    click_sound.play()
                    audio()
                if VIDEO_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    click_sound.play()
                    video()
                if KEY_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    click_sound.play()
                    key()
                    
        pygame.display.update()

def audio():
    while True:
        
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        
        SCREEN.blit(BG,(0, 0))
        
        OPTIONS_BACK = Button(image=None, pos=(180, 500), 
                            text_input="Back", font=get_font_1(75), base_color="White", hovering_color="Red")
        
        for button in [OPTIONS_BACK]:    
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    click_sound.play()
                    options()                  
                           
        pygame.display.update()

def video():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        
        SCREEN.blit(BG,(0, 0))
        
        OPTIONS_BACK = Button(image=None, pos=(180, 500), 
                            text_input="Back", font=get_font_1(75), base_color="White", hovering_color="Red")
        
        for button in [OPTIONS_BACK]:    
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    click_sound.play()
                    options()                  
                           
        pygame.display.update()

def key():
    while True:
        
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        
        SCREEN.blit(BG,(0, 0))
        
        OPTIONS_BACK = Button(image=None, pos=(180, 500), 
                            text_input="Back", font=get_font_1(75), base_color="White", hovering_color="Red")
        
        for button in [OPTIONS_BACK]:    
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    click_sound.play()
                    options()                  
                           
        pygame.display.update()     
      
def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font_1(100).render("NEON VEIL", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(300, 100))

        PLAY_BUTTON = Button(image=None, pos=(150, 300), 
                            text_input="PLAY", font=get_font_1(75), base_color="#d7fcd4", hovering_color="yellow")
        OPTIONS_BUTTON = Button(image=None, pos=(200, 400), 
                            text_input="OPTIONS", font=get_font_1(75), base_color="#d7fcd4", hovering_color="yellow")
        QUIT_BUTTON = Button(image=None, pos=(150, 500), 
                            text_input="QUIT", font=get_font_1(75), base_color="#d7fcd4", hovering_color="red")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    click_sound.play()
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    click_sound.play()
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()