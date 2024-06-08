import pygame
import sys
from button import Button
from pygame import mixer
import json

pygame.init()
pygame.mixer.init()

# Load the click sound
click_sound = pygame.mixer.Sound("assets/enterface_click_2.mp3")

# Create the screen and set the title
SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

# Colors for Slider
BG_COLOR = (30, 30, 30)
SLIDER_COLOR = (200, 200, 200)
HANDLE_COLOR = ("#b68f40")

# Background
BG = pygame.image.load("assets/Background.png")

# Fonts
def get_font_1(size):
    return pygame.font.Font("assets/cyb3.ttf", size)

def get_font_2(size):
    return pygame.font.Font("assets/cyb_options.otf", size)

#class for slider
class Slider:
    def __init__(self, x, y, width, height, handle_width, initial_pos=0.5):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.handle_width = handle_width
        self.pos = initial_pos
        self.dragging = False

    def draw(self, screen):
        pygame.draw.rect(screen, SLIDER_COLOR, (self.x, self.y, self.width, self.height))
        handle_x = self.x + self.pos * (self.width - self.handle_width)
        pygame.draw.rect(screen, HANDLE_COLOR, (handle_x, self.y - 5, self.handle_width, self.height + 10))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            handle_x = self.x + self.pos * (self.width - self.handle_width)
            if handle_x <= mouse_x <= handle_x + self.handle_width and self.y - 5 <= mouse_y <= self.y + self.height + 5:
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mouse_x, _ = event.pos
            self.pos = (mouse_x - self.x) / (self.width - self.handle_width)
            self.pos = max(0.0, min(1.0, self.pos))

    def get_value(self):
        return self.pos
    
#Define of save and load volume when changed 
def save_volume_settings(volume_settings):
    with open("volume_settings.json", "w") as f:
        json.dump(volume_settings, f)

def load_volume_settings():
    try:
        with open("volume_settings.json", "r") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        return {"music_volume": 0.5, "effects_volume": 0.5}  

# Options 
def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(BG, (0, 0))

        OPTIONS_TEXT = get_font_1(100).render("OPTIONS", True, "#b68f40")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 60))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        AUDIO_BUTTON = Button(image=None, pos=(180, 200), text_input="Audio", font=get_font_1(75), base_color="White", hovering_color="Yellow")
        VIDEO_BUTTON = Button(image=None, pos=(180, 300), text_input="Video", font=get_font_1(75), base_color="White", hovering_color="Yellow")
        KEY_BUTTON = Button(image=None, pos=(318, 400), text_input="Key Bindings", font=get_font_1(75), base_color="White", hovering_color="Yellow")
        OPTIONS_BACK = Button(image=None, pos=(180, 600), text_input="Back", font=get_font_1(75), base_color="White", hovering_color="Red")

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

#Audio
def audio():
    volume_settings = load_volume_settings()
    music_volume_slider = Slider(800, 200, 300, 20, 15, initial_pos=volume_settings.get("music_volume", 0.5))
    effects_volume_slider = Slider(800, 300, 300, 20, 15, initial_pos=volume_settings.get("effects_volume", 0.5))
    
    lobby = pygame.mixer.Sound("assets/Wild_Hunt.wav")
    lobby.play(-1)
    lobby.set_volume(volume_settings.get("music_volume", 0.5))
    
    def update_volume():
        volume_settings["music_volume"] = music_volume_slider.get_value()
        volume_settings["effects_volume"] = effects_volume_slider.get_value()
        lobby.set_volume(volume_settings["music_volume"])
        save_volume_settings(volume_settings)
    running = True
    while running:
        SCREEN.blit(BG, (0, 0))
        
        # Volume Audio Text
        MUSIC_TEXT = get_font_1(55).render("Music Volume", True, "#FFFFF0")
        MUSIC_RECT = MUSIC_TEXT.get_rect(center=(250, 200))
        SCREEN.blit(MUSIC_TEXT, MUSIC_RECT)
        music_volume_slider.draw(SCREEN)

        EFFECTS_TEXT = get_font_1(55).render("Effects Volume", True, "#FFFFF0")
        EFFECTS_RECT = EFFECTS_TEXT.get_rect(center=(250, 300))
        SCREEN.blit(EFFECTS_TEXT, EFFECTS_RECT)
        effects_volume_slider.draw(SCREEN)
        
        #Audio Main Text
        PLAY_TEXT = get_font_1(110).render("Audio", True, "#b68f40")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 60))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        # Back Button 
        OPTIONS_BACK = Button(image=None, pos=(180, 600), text_input="Back", font=get_font_1(75), base_color="White", hovering_color="Red")
        OPTIONS_BACK.changeColor(pygame.mouse.get_pos())
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(pygame.mouse.get_pos()):
                    volume_settings["music_volume"] = music_volume_slider.get_value()
                    volume_settings["effects_volume"] = effects_volume_slider.get_value()
                    lobby.set_volume(volume_settings["music_volume"])
                    save_volume_settings(volume_settings)
                    click_sound.play()
                    #Go back to options menu
                    options()
            music_volume_slider.handle_event(event)
            effects_volume_slider.handle_event(event)
        pygame.display.flip()

#Video
def video():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(BG, (0, 0))

        PLAY_TEXT = get_font_1(110).render("Video", True, "#b68f40")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 60))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        OPTIONS_BACK = Button(image=None, pos=(180, 600), text_input="Back", font=get_font_1(75), base_color="White", hovering_color="Red")
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

#Key Bindings
def key():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(BG, (0, 0))

        PLAY_TEXT = get_font_1(100).render("Key Bindings", True, "#b68f40")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 60))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        OPTIONS_BACK = Button(image=None, pos=(180, 600), text_input="Back", font=get_font_1(75), base_color="White", hovering_color="Red")
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

#main menu lobby 
def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font_1(100).render("NEON VEIL", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(300, 100))

        PLAY_BUTTON = Button(image=None, pos=(150, 300), text_input="PLAY", font=get_font_1(75), base_color="#d7fcd4", hovering_color="yellow")
        OPTIONS_BUTTON = Button(image=None, pos=(200, 400), text_input="OPTIONS", font=get_font_1(75), base_color="#d7fcd4", hovering_color="yellow")
        QUIT_BUTTON = Button(image=None, pos=(150, 500), text_input="QUIT", font=get_font_1(75), base_color="#d7fcd4", hovering_color="red")

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
                    import level_1
                    level_1.main()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    click_sound.play()
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()
