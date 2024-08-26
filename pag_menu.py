import pygame, sys
from character import entidade
from alglin import *
from consts import res

class Menu():
    def init(self, window, state):

        config = ""
        self.window = window

        pygame.display.set_caption('Pombos brabos')

        self.state = {
        }

        self.clock = pygame.time.Clock()

        background = pygame.image.load(r"assets\Title_Image_Day.png")
        self.background = pygame.transform.scale(background, self.window.get_size())
        
        self.window.fill("grey")

        self.play_bt = entidade(0,0,10,10,"rect","play_bt")
        self.play_bt.center(res)

        self.title = entidade(0,0,10,10,"rect","title")
        self.pombo = entidade(0,0,10,10, "rect", "pombo")
        self.pombo.invert_x_axis()
        
        pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
        self.my_font = pygame.font.SysFont('Comic Sans MS', 30)

        self.seta1 = entidade(0,0,0,0,"rect", "seta")
        self.seta1.invert_x_axis()
        self.seta2 = entidade(0,0,0,0,"rect", "seta")

        self.traj = []

        pass

    def loop(self, state):
        #     V eventos V
        mbd = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mbd = True

        self.play_bt.center(res, [0.2,-0.1])
        self.title.center(res,[0,0.3])
        self.pombo.center(res,[-0.2,-0.03])
        self.seta1.center(res, [-0.16, -0.12])
        self.seta2.center(res, [-0.24, -0.12])

        mouse_x, mouse_y = pygame.mouse.get_pos()

        if self.play_bt.hover_check(mouse_x, mouse_y):
            self.play_bt.set_action("hover")
            if mbd:
                state["skin"] = self.pombo.skin
                return "instrucoes"
        else:
            self.play_bt.set_action("idle")

        if self.seta1.hover_check(mouse_x, mouse_y):
            self.seta1.set_action("hover")
            if mbd:
                self.pombo.change_skin(dec=True)
        else:
            self.seta1.set_action("idle")

        if self.seta2.hover_check(mouse_x, mouse_y):
            self.seta2.set_action("hover")
            if mbd:
                self.pombo.change_skin(inc=True)
        else:
            self.seta2.set_action("idle")


        # -------------------- 

        # V geracao de imagens V

        self.window.blit(self.background, (0,0))
        self.play_bt.blit(self.window)
        self.title.blit(self.window)
        self.pombo.blit(self.window)
        self.seta1.blit(self.window)
        self.seta2.blit(self.window)
        # pygame.draw.rect(self.window, "red", self.seta1.obj.rect )



        # --------------------

        pygame.display.update()
        dt = self.clock.tick(100) / 1000

        return "pass"
