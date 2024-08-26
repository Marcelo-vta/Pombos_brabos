import pygame, sys
from character import entidade, colide, path_preview
from alglin import *
import numpy as np

res = (1280,720)
grav = np.array([0,0.1])

class fase1():
    def init(self, window, state):
        """
        Inicializa todas as informações e objetos do jogo.
        """

        pygame.init()

        config = ""

        # window = pygame.display.set_mode(tuple(asset['tam_tela']), vsync=True, flags=pygame.SCALED)
        self.window = window

        pygame.display.set_caption('Pombos brabos')

        self.clock = pygame.time.Clock()

        background = pygame.image.load(r"assets\Title_Image_Day.png")
        self.background = pygame.transform.scale(background, self.window.get_size())

        self.pombo = entidade(0,0,10,10,"rect","pombo", scale=0.6)
        self.pombo.change_skin(state["skin"])
        self.pombo.set_action("sitting")

        self.rua = entidade(0,0,10,10,"rect","rua")

        self.poste = entidade(0,0,10,10,"rect","poste")

        self.i = 0

        self.entidades = []

        self.entidades += [self.rua, self.pombo, self.poste]

        self.rua.center(res, [0, -0.45])
        self.poste.center(res, [0.35, -0.087])
        self.pombo.center(res, [0.275, 0.11])

        self.p_initial = self.pombo.x, self.pombo.y

        self.pombo.invert_x_axis()
        self.pulling = False

        pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
        self.my_font = pygame.font.SysFont('Comic Sans MS', 30)

        self.shit = None
        self.path = None
        self.landed = False
        self.reset = False
        self.counter = 0

        pass
    
    def loop(self, state):
        #     V eventos V

        mouse_dist = 0
        
        mouse_x, mouse_y = pygame.mouse.get_pos()

        mbd = False
        mbu = False
        launch = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mbd = True
            if event.type == pygame.MOUSEBUTTONUP:
                mbu = True

        if self.landed:
            if self.reset:
                if self.counter >= 2:
                    direct = vetor_direcao(np.array([self.pombo.x, self.pombo.y]), np.array(self.p_initial))
                    vel = 10
                    self.pombo.vel = direct*vel
                    if dist(np.array([self.pombo.x, self.pombo.y]), np.array(self.p_initial)) < 5:
                        self.landed = False
                        self.reset = False
                        self.pombo.set_action("sitting")
                        self.pombo.vel = np.array([0.0,0.0])
                        self.pombo.accel = np.array([0.0,0.0])
                        self.pombo.move(float(self.p_initial[0]), float(self.p_initial[1]))
            else:
                if self.counter >= 3:
                    self.pombo.set_action("idle")
                    if self.pombo.obj.center[0] <= res[0]/2:
                        self.pombo.vel = np.array([-10,0])
                    else:
                        self.pombo.vel = np.array([10,0])
                    if not colide(self.pombo.obj, [self.rua.obj]):
                        self.reset = True
                        self.counter = 0
                        self.pombo.move(float(-self.pombo.obj.width), float(-self.pombo.obj.height))
                        self.pombo.set_action("flying")
            pass
        else:

            if self.pombo.hover_check(mouse_x, mouse_y):
                if self.pombo.action == "sitting":
                    if mbd:
                        self.pulling = True

                
            
            if self.pulling:
                    
                self.pombo.set_action("idle")
                dir_vet = vetor_direcao(np.array([mouse_x, mouse_y]), np.array(self.pombo.obj.center))
                mouse_dist = dist(np.array([mouse_x, mouse_y]), np.array(self.pombo.obj.center))*0.1
                launch_vet = dir_vet * mouse_dist

                if mbu:
                    self.pulling = False
                    if not self.pombo.hovered:
                        launch = True
                        self.path = None
                else:
                    if not self.pombo.hovered:
                        self.path = path_preview(dir_vet, mouse_dist, grav, np.array(self.pombo.obj.center))

            if launch:
                self.pombo.set_action("flying")
                self.pombo.vel += launch_vet
                self.pombo.accel += grav

            if self.pombo.action == "flying":
                if mbd:
                    self.shit = entidade(self.pombo.obj.center[0], self.pombo.obj.center[1], 1,1,"rect","bosta", scale=0.6)
                    self.shit.vel += np.array([0,20]) + self.pombo.vel * np.array([1,0])
                    self.shit.accel += grav
            
            if self.shit != None:
                self.shit.vel += self.shit.accel
                b_coords = np.array([self.shit.x, self.shit.y])
                b_coords += (self.shit.vel*0.2)
                self.shit.move(b_coords[0], b_coords[1])

            if self.rua.obj.rect.collidepoint(self.pombo.obj.center[0],self.pombo.obj.center[1]+10):
                self.landed = True
                self.counter = 0
                self.pombo.set_action("sitting")
                self.pombo.vel = np.array([0,0])
                self.pombo.accel = np.array([0,0])

        # -------------------- 

        # V geracao de imagens V

        self.pombo.vel += self.pombo.accel
        p_coords = np.array([self.pombo.x, self.pombo.y])
        p_coords += (self.pombo.vel*0.2)
        self.pombo.move(p_coords[0], p_coords[1])

        if self.pombo.vel[0] < 0:
            if self.pombo.inverted:
                self.pombo.inverted = False
        else:
            if not self.pombo.inverted:
                self.pombo.inverted = True

        text_surface = self.my_font.render(str(""), False, "black")

        self.window.blit(self.background, (0,0))
        self.rua.blit(self.window)
        self.poste.blit(self.window)
        if self.shit != None:
            self.shit.blit(self.window)
        if self.path != None:
            self.path.blit(self.window)
        self.pombo.blit(self.window)
        self.window.blit(text_surface, (20,20))
        
        # --------------------

        pygame.display.update()
        dt = self.clock.tick(60)/1000
        self.counter += dt


        self.i += 1


        return True



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
                return False
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
        text_surface = self.my_font.render(str(mbd), False, "black")

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
        print(dt)

        return True
