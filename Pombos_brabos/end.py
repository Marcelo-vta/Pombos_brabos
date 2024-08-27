import pygame
import sys
from Pombos_brabos.consts import title_image_day

class end():
    def init(self, window, state):

        config = ""
        self.window = window

        pygame.display.set_caption('Pombos brabos')

        self.state = {
        }

        self.clock = pygame.time.Clock()

        background = pygame.image.load(title_image_day)
        self.background = pygame.transform.scale(background, self.window.get_size())
    
    def loop(self, state):
        #     V eventos V
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        self.window.blit(self.background, (0,0))

        pygame.display.update()
        dt = self.clock.tick(100) / 1000

        return "pass"


        

