import sys
import pygame

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Neon Veil')
        self.screen = pygame.display.set_mode((861,504))

        self.clock = pygame.time.Clock()

        self.image = pygame.image.load('images/background1.jpg')

    def run(self):
        while True :
            self.screen.blit(self.image,(0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            self.clock.tick(60)

Game().run()