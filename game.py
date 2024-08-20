import pygame, sys
from character import entidade, colide

class fase1():
    def __init__(self, window, assets):
        """
        Inicializa todas as informações e objetos do jogo.
        """

        pygame.init()

        config = ""


        # window = pygame.display.set_mode(tuple(asset['tam_tela']), vsync=True, flags=pygame.SCALED)
        self.window = window

        pygame.display.set_caption('Pombos brabos')

        self.state = {
        }

        self.clock = pygame.time.Clock()

        background = pygame.image.load(r"Pombos_brabos\assets\Title_Image_Day.png")
        background = pygame.transform.scale(background, self.window.get_size)

        self.window.fill("grey")
        self.assets = assets

        pass

    def loop(self):
        #     V eventos V

        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # -------------------- 

        # V geracao de imagens V

        self.window.blit(self.assets["background"], (0,0))

        # --------------------

        pygame.display.update()
        dt = self.clock.tick(100) / 1000



    # def atualiza_estado(window, asset, state):
    #     """
    #     Atualiza estado do jogo, e checa ações e interações.
    #     """        
    #     return True

    # def game_loop(window, asset, state):
    #     """
    #     Loop principal do jogo, onde roda todas as outras funções necessárias.
    #     """
    #     game = True
    #     while game:
    #         game = atualiza_estado(window, asset, state)
    #         pass
    #         pygame.display.update()

class menu():
    def __init__(self, window):

        config = ""
        self.window = window

        pygame.display.set_caption('Pombos brabos')

        self.state = {
        }

        self.clock = pygame.time.Clock()

        background = pygame.image.load(r"Pombos_brabos\assets\Title_Image_Day.png")
        self.background = pygame.transform.scale(background, self.window.get_size())
        
        self.window.fill("grey")


        pass

    def loop(self):
        #     V eventos V

        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # -------------------- 

        # V geracao de imagens V

        self.window.blit(self.background, (0,0))

        self.window.blit(self.assets["title"], (self.window.get_width()/2 - self.assets["title"].get_width()/2, self.window.get_height()/4 - self.assets["title"].get_height()/2))

        # --------------------

        pygame.display.update()
        dt = self.clock.tick(100) / 1000
