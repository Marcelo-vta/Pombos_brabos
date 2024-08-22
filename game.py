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

        background = pygame.image.load(r"assets\Title_Image_Day.png")
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

        background = pygame.image.load(r"assets\Title_Image_Day.png")
        self.background = pygame.transform.scale(background, self.window.get_size())
        
        self.window.fill("grey")

        self.butao = entidade(0,0,10,10,"rect","pombo")
        
        pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
        self.my_font = pygame.font.SysFont('Comic Sans MS', 30)


        pass

    def loop(self):
        #     V eventos V

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x in range(0,100):
            self.butao.set_action("hover")


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.butao.set_action("sitting")
                if event.button == 3:
                    self.butao.skin += 1

        # -------------------- 

        # V geracao de imagens V
        text_surface = self.my_font.render(str(self.butao.frame), False, "black")

        self.window.blit(self.background, (0,0))
        self.butao.blit(self.window)
        self.window.blit(text_surface, (100,100))
        # pygame.draw.rect(self.window, "red", self.butao.obj.rect )



        # --------------------

        pygame.display.update()
        dt = self.clock.tick(100) / 1000
