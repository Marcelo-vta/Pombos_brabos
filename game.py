import pygame, sys
from character import entidade, colide, path_preview
from alglin import *
import numpy as np
from instrucoes import Instrucoes

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

        self.pombo = entidade(0,0,10,10,"rect","pombo", mass=100, scale=0.6)
        self.pombo.change_skin(state["skin"])
        self.pombo.set_action("sitting")

        self.humano = entidade(0,0,10,10,"rect","humano")

        self.rua = entidade(0,0,10,10,"rect","rua")

        self.poste = entidade(0,0,10,10,"rect","poste")

        self.wall = entidade(0,0,10,10,"rect","wall")
        self.wall.set_action("4")

        self.i = 0

        self.entidades = []

        self.entidades += [self.rua, self.pombo, self.poste]

        self.rua.center(res, [0, -0.45])
        self.poste.center(res, [0.35, -0.087])
        self.pombo.center(res, [0.275, 0.11])
        self.wall.center(res, [0, -0.175])

        
        self.humano.invert_x_axis()
        self.humano.center(res, [-0.35, -0.33])

        self.sol = entidade(0,0, 20, 20, 'circle', 'sol', mass=10000)
        self.sol.center(res, [0.0, 0.5])
        self.mola = entidade(0,0,10,10,'rect','mola', mass=100, rot='y', scale=0.8)
        self.mola.center(res, (0,-0.35))

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

        self.paused = False

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not(self.paused)
                    pause_screen = pygame.Surface(res)
                    pause_screen.fill((0, 0, 0))
                    pause_screen.set_alpha(150)
                    self.window.blit(pause_screen, (0, 0))

        if self.paused:
            retomar = entidade(0,0,10,10,"rect","retomar")
            retomar.center(res, [0,0.3])
            if retomar.hover_check(mouse_x, mouse_y):
                retomar.set_action("hover")
                if mbd:
                    self.paused = False

            recomecar = entidade(0,0,10,10,"rect","recomecar")
            recomecar.center(res)
            if recomecar.hover_check(mouse_x, mouse_y):
                recomecar.set_action("hover")
                if mbd:
                    return "stage1"
                
            voltar = entidade(0,0,10,10,"rect","voltar")
            voltar.center(res, [0,-0.3])
            if voltar.hover_check(mouse_x, mouse_y):
                voltar.set_action("hover")
                if mbd:
                    return "menu"

            retomar.blit(self.window)
            recomecar.blit(self.window)
            voltar.blit(self.window)

        else:
            if self.landed:

                self.sol.vel = np.array([0.0, 0.0])
                self.sol.accel = np.array([0.0, 0.0])

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
                            self.shit = None
                else:
                    if self.counter >= 3:
                        self.pombo.set_action("idle")
                        if self.pombo.obj.center[0] <= res[0]/2:
                            self.pombo.vel = np.array([-10.0,0.0])
                        else:
                            self.pombo.vel = np.array([10.0,0.0])
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
                        self.path = None
                        self.pombo.set_action("sitting")
                        if not self.pombo.hovered:
                            launch = True
                    else:
                        if not self.pombo.hovered:
                            self.path = path_preview(dir_vet, mouse_dist, grav, np.array(self.pombo.obj.center))
                        else:
                            self.path = None

                if launch:
                    self.pombo.set_action("flying")
                    self.pombo.vel += launch_vet
                    self.pombo.accel += grav

                if self.pombo.action == "flying":
                    acc_grav = acc_gravitacional(np.array([self.sol.x, self.sol.y]), np.array([self.pombo.x, self.pombo.y]), self.sol.mass, self.pombo.mass)
                    self.pombo.accel = grav + acc_grav[0]*vetor_direcao(np.array([self.pombo.x, self.pombo.y]), np.array([self.sol.x, self.sol.y]))
                    self.sol.accel = acc_grav[1]*vetor_direcao(np.array([self.sol.x, self.sol.y]), np.array([self.pombo.x, self.pombo.y]))

                    if mbd:
                        if self.shit == None:
                            self.shit = entidade(self.pombo.obj.center[0], self.pombo.obj.center[1], 1,1, "rect", "bosta", scale=0.6)
                            self.shit.vel += np.array([0,20]) + self.pombo.vel * np.array([1,0])
                            self.shit.accel += grav
                    if colide(self.pombo.obj, [self.wall.obj]):
                        self.landed = True
                        self.reset = True
                        self.counter = 2
                        self.pombo.accel = np.array([0.0,0.0])
                        self.pombo.vel = np.array([0.0,0.0])
                        
                
                if self.shit != None:
                    self.shit.vel += self.shit.accel
                    b_coords = np.array([self.shit.x, self.shit.y])
                    b_coords += (self.shit.vel*0.2)
                    self.shit.move(b_coords[0], b_coords[1])

                    if colide(self.shit.obj, [self.humano.obj]):
                        self.shit.set_action("hit")
                        self.shit.vel = np.array([0.0,0.0])
                        self.shit.accel = np.array([0.0,0.0])
                        self.humano.set_action("hit")
                    
                    if colide(self.shit.obj, [self.rua.obj]):
                        self.shit.set_action("hit")
                        self.shit.vel = np.array([0.0,0.0])
                        self.shit.accel = np.array([0.0,0.0])

                    if self.shit.action == "hit":
                        if self.shit.frame == 4:
                            self.shit = None

                if self.rua.obj.rect.collidepoint(self.pombo.obj.center[0],self.pombo.obj.center[1]+10):
                    self.landed = True
                    self.counter = 0
                    self.pombo.set_action("sitting")
                    self.pombo.vel = np.array([0.0,0.0])
                    self.pombo.accel = np.array([0.0,0.0])
                
                if self.pombo.x > res[0] or self.pombo.x < -self.pombo.width:
                    self.sol.vel = np.array([0.0, 0.0])
                    self.sol.accel = np.array([0.0, 0.0])
                    self.landed = True
                    self.reset = True
                    self.counter = 0
                    self.pombo.move(float(-self.pombo.obj.width), float(-self.pombo.obj.height))
                    self.pombo.set_action("flying")

        # --------------------
            if colide(self.pombo.obj, [self.mola.obj]) and self.mola.action == "idle":
                self.pombo.vel = acc_elastica(self.pombo.vel, self.mola.rotation)
                self.mola.set_action("active")
                
            if self.mola.action == "active" and self.mola.frame >= len(self.mola.find_sequence())-1:
                self.mola.set_action("idle")

            # V geracao de imagens V

        
            self.pombo.vel += self.pombo.accel
            p_coords = np.array([self.pombo.x, self.pombo.y])
            p_coords += (self.pombo.vel*0.2)
            self.pombo.move(p_coords[0], p_coords[1])

            self.sol.vel += self.sol.accel
            p_coords = np.array([self.sol.x, self.sol.y])
            p_coords += (self.sol.vel*0.2)
            self.sol.move(p_coords[0], p_coords[1])

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
            self.humano.blit(self.window)
            self.mola.blit(self.window)
            self.wall.blit(self.window)
            self.sol.blit(self.window)
            self.pombo.blit(self.window)
            # self.window.blit(text_surface, (20,20))
        # pygame.draw.rect(self.window, (255,0,0,60), self.mola.obj.rect)
            # if self.shit != None:
            #     pygame.draw.rect(self.window, (255,0,0,60), self.shit.obj.rect)
            
        # --------------------

        pygame.display.update()
        dt = self.clock.tick(60)/1000
        self.counter += dt


        self.i += 1


        return "pass"



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

        return "pass"
