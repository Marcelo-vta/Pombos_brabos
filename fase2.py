import pygame, sys
from character import entidade, colide, path_preview
from alglin import *
import numpy as np
from consts import res, grav

class Fase2():
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

        background = pygame.image.load(r"Pombos_brabos/assets/Title_Image_Day.png")
        self.background = pygame.transform.scale(background, self.window.get_size())

        self.pombo = entidade(0,0,10,10,"rect","pombo", mass=100, scale=0.6)
        self.pombo.change_skin(state["skin"])
        self.pombo.set_action("sitting")

        self.humano = entidade(0,0,10,10,"rect","humano")

        self.rua = entidade(0,0,10,10,"rect","rua")

        self.poste = entidade(0,0,10,10,"rect","poste")

        self.wall1 = entidade(0,0,10,10,"rect","wall")
        self.wall1.set_action("3")

        self.wall2 = entidade(0,0,10,10,"rect","wall")
        self.wall2.set_action("1")
        self.wall2.invert_y_axis()

        self.i = 0

        self.entidades = []

        self.entidades += [self.rua, self.pombo, self.poste]

        self.rua.center(res, [0, -0.45])
        self.poste.center(res, [0.35, -0.087])
        self.pombo.center(res, [0.275, 0.11])
        self.wall1.center(res, [-0.09, -0.083])
        self.wall2.center(res, [-0.4, 0.3])

        self.humano.center(res, [-0.15, -0.33])


        self.mola1 = entidade(0,0,10,10,'rect','mola', mass=100, rot='x', scale=0.8)
        self.mola1.center(res, (-0.34,0.15))
        self.mola1.rotate_sprite(90)

        self.mola2 = entidade(0,0,10,10,'rect','mola', mass=100, rot='x', scale=0.8)
        self.mola2.center(res, (-0.136,0.0))
        self.mola2.rotate_sprite(270)

        self.mola3 = entidade(0,0,10,10,'rect','mola', mass=100, rot='x', scale=0.8)
        self.mola3.center(res, (-0.34,-0.15))
        self.mola3.rotate_sprite(90)
        
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
        self.end = False
        self.endcounter = -1

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
            if self.endcounter >= 11:
                return "end"
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
                    if mbd:
                        if self.shit == None:
                            self.shit = entidade(self.pombo.obj.center[0], self.pombo.obj.center[1], 1,1, "rect", "bosta", scale=0.6)
                            self.shit.vel += np.array([0,20]) + self.pombo.vel * np.array([1,0])
                            self.shit.accel += grav
                    if colide(self.pombo.obj, [self.wall1.obj]):
                        self.landed = True
                        self.reset = True
                        self.counter = 2
                        self.pombo.accel = np.array([0.0,0.0])
                        self.pombo.vel = np.array([0.0,0.0])
                    if colide(self.pombo.obj, [self.wall2.obj]):
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
                        self.endcounter += 1
                    
                    if colide(self.shit.obj, [self.rua.obj]):
                        self.shit.set_action("hit")
                        self.shit.vel = np.array([0.0,0.0])
                        self.shit.accel = np.array([0.0,0.0])
                    if colide(self.shit.obj, [self.wall1.obj]):
                        self.shit.set_action("hit")
                        self.shit.vel = np.array([0.0,0.0])
                        self.shit.accel = np.array([0.0,0.0])
                    if colide(self.shit.obj, [self.wall2.obj]):
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
                    self.landed = True
                    self.reset = True
                    self.counter = 0
                    self.pombo.move(float(-self.pombo.obj.width), float(-self.pombo.obj.height))
                    self.pombo.set_action("flying")

        # --------------------
            if colide(self.pombo.obj, [self.mola1.obj]) and self.mola1.action == "idle":
                self.pombo.vel = acc_elastica(self.pombo.vel, self.mola1.rotation)
                self.mola1.set_action("active")
                
            if self.mola1.action == "active" and self.mola1.frame >= len(self.mola1.find_sequence())-1:
                self.mola1.set_action("idle")

            if colide(self.pombo.obj, [self.mola2.obj]) and self.mola2.action == "idle":
                self.pombo.vel = acc_elastica(self.pombo.vel, self.mola2.rotation)
                self.mola2.set_action("active")
                
            if self.mola2.action == "active" and self.mola2.frame >= len(self.mola2.find_sequence())-1:
                self.mola2.set_action("idle")

            if colide(self.pombo.obj, [self.mola3.obj]) and self.mola3.action == "idle":
                self.pombo.vel = acc_elastica(self.pombo.vel, self.mola3.rotation)
                self.mola3.set_action("active")
                
            if self.mola3.action == "active" and self.mola3.frame >= len(self.mola3.find_sequence())-1:
                self.mola3.set_action("idle")

            # V geracao de imagens V

            print(self.pombo.vel, self.pombo.accel)
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
            self.humano.blit(self.window)
            self.mola1.blit(self.window)
            self.mola2.blit(self.window)
            self.mola3.blit(self.window)
            self.wall1.blit(self.window)
            self.wall2.blit(self.window)
            if self.shit != None:
                self.shit.blit(self.window)
            if self.path != None:
                self.path.blit(self.window)
            self.pombo.blit(self.window)
            # self.window.blit(text_surface, (20,20))
        # pygame.draw.rect(self.window, (255,0,0,60), self.mola.obj.rect)
            # if self.shit != None:
            #     pygame.draw.rect(self.window, (255,0,0,60), self.shit.obj.rect)
            
        # --------------------
        print(self.endcounter)
        pygame.display.update()
        dt = self.clock.tick(60)/1000
        self.counter += dt
        if self.endcounter >= 0:
            self.endcounter += dt


        self.i += 1


        return "pass"