import pygame
import numpy as np
from alglin import *

# -----------------------------------------------------------------------------------------------------------------------
#                                                 V papo de animação V

animation_db = {}
animation_type = {}

def load_animations():
    assets_path = "assets/"

    global animation_db 
    global animation_type
    
    with open(assets_path+"animations.txt") as r:
        animations = r.read().split("\n")
    
    for i in range(len(animations)):
        animations[i] = animations[i].split(" ")

    for inf in animations:
        e_type = inf[0].split("/")[0]
        print(inf)
        frames = [int(i) for i in inf[1].split(";")]
        state = inf[0].split('/')[1]
        endcode = inf[4]
        scale = inf[3]
        a_type = inf[2]

        if e_type not in animation_db:
            animation_db[e_type] = {}
            animation_type[e_type] = {}
    

        if e_type == "pombo":
            state = inf[0].split('/')[2]
            for i in range(9):
                if str(i) not in animation_db[e_type]:
                    animation_db[e_type][str(i)] = {}
                    animation_type[e_type][str(i)] = {}
                animation_db[e_type][str(i)][state] = []
                animation_type[e_type][str(i)][state] = a_type
                for j in range(len(frames)):
                    for _ in range(frames[j]):
                        sprite = pygame.image.load(f"{assets_path}{e_type}/{str(i)}/{state}/{str(j)}{endcode}")
                        sprite = pygame.transform.scale_by(sprite, float(scale))
                        animation_db[e_type][str(i)][state].append(sprite)
        else:
            animation_db[e_type][inf[0].split("/")[1]] = []
            animation_type[e_type][inf[0].split("/")[1]] = a_type
            for j in range(len(frames)):
                for _ in range(frames[j]):
                    sprite = pygame.image.load(f"{assets_path}{e_type}/{state}/{str(j)}{endcode}")
                    sprite = pygame.transform.scale_by(sprite, float(scale))
                    animation_db[e_type][state].append(sprite)

def anim_db():
    return animation_db

def anim_type():
    return animation_type

# -----------------------------------------------------------------------------------------------------------------------
#                                           V Colisãao de objetos V

def intersec_rect_rect(rect1, rect2):
    return rect1.colliderect(rect2)
def intersec_circ_rect(circ, rect):
    if not (circ.center[0] <= rect.x + rect.width + circ.rad and circ.center[0] >= rect.x - circ.rad):
        return False
    if not (circ.center[1] <= rect.y + rect.height + circ.rad and circ.center[1] >= rect.y - circ.rad):
        return False
    return True
def intersec_circ_circ(circ1, circ2):
    return (((circ1.center[0]-circ2.center[0])**2 + (circ1.center[1]-circ2.center[1])**2)**0.5) <= circ1.rad + circ2.rad


def colide(objeto, lista_objs):
    colisoes = []
    for obj_comp in lista_objs:
        collision = {"x": False, "y": False}
        if objeto.collide_method == "rect":
            if obj_comp.collide_method == "rect":
                if intersec_rect_rect(objeto.rect, obj_comp.rect):
                    if obj_comp not in colisoes:
                        colisoes.append(obj_comp)
                else:
                    if obj_comp in colisoes:
                        colisoes.remove(obj_comp)
            else:
                if intersec_circ_rect(obj_comp.circle, objeto.rect):
                    if obj_comp not in colisoes:
                        colisoes.append(obj_comp)
                else:
                    if obj_comp in colisoes:
                        colisoes.remove(obj_comp)
        else:
            if obj_comp.collide_method == "rect":
                if intersec_circ_rect(objeto.circle, obj_comp.rect):
                    if obj_comp not in colisoes:
                        colisoes.append(obj_comp)
                else:
                    if obj_comp in colisoes:
                        colisoes.remove(obj_comp)
            else:
                if intersec_circ_circ(obj_comp.circle, objeto.circle):
                    if obj_comp not in colisoes:
                        colisoes.append(obj_comp)
                else:
                    if obj_comp in colisoes:
                        colisoes.remove(obj_comp)
    return colisoes

# ------------------------------------------------------------------------------------------------------------------------

class entidade(object):
    def __init__(self, x, y, width, height, collide_method, e_type, scale=1):

        self.scale = scale

        valid = {"rect", "circle"}
        if collide_method not in valid:
            raise ValueError("results: status must be one of %r." % valid)

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.collide_method = collide_method
        self.vel = np.array([0.0,0.0])
        self.accel = np.array([0.0,0.0])
        self.type = e_type

        self.rotation = 0
        self.state = 0
        self.collide_list = []
        self.obj = obj(x, y, self.width, self.height, collide_method)

        self.action = "idle"
        self.frame = 0
        self.set_action("idle")
        self.skin = 0

        self.inverted = False

        self.a_type = "loop"
        self.advance_frame(True)
        self.hovered = False


        pass

    def find_sequence(self):
        global animation_db

        busca = animation_db[self.type]
        a_type = animation_type[self.type]
        if self.type == "pombo":
            busca = busca[str(self.skin)]
            a_type = a_type[str(self.skin)]
        
        self.a_type = a_type[self.action]
        return busca[self.action]
    
    def set_frame(self, new_frame):
        self.frame = new_frame % len(self.find_sequence())
    
    def advance_frame(self, changed=False):
        sequence = self.find_sequence()
        self.frame += 1

        if self.a_type == "loop":
            inc = 0
        else:
            inc = len(sequence)-1

        if self.frame >= len(sequence):
            self.frame = inc

        frame = sequence[self.frame]
        frame = pygame.transform.scale_by(frame, self.scale)

        if frame.get_width != self.width:
            self.width = frame.get_width()
            changed = True

        if frame.get_height != self.height:
            self.height = frame.get_height()
            changed = True

        if changed:
            self.obj.dimensions(self.width, self.height)

    def center(self, res, offset = [0,0]):
        self.move((res[0]/2)-(self.width/2)-(res[0]*offset[0]), (res[1]/2)-(self.height/2)-(res[1]*offset[1]))

    def change_skin(self, new_skin=0, inc=False, dec=False):
        if self.type == "pombo":
            if inc:
                if self.skin == 8:
                    self.skin = 0
                else:
                    self.skin += 1
                return

            if dec:
                if self.skin == 0:
                    self.skin = 8
                else:
                    self.skin -= 1
                return

            if new_skin in range(0,9):
                self.skin = new_skin
                return
    
    def set_action(self, action):
        if self.action != action:
            self.frame = 0
            self.action = action
    
    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
        self.obj.update(new_x, new_y)

    def blit(self, window):
        sequence = self.find_sequence()
        frame = sequence[self.frame]
        if self.inverted:
            frame = pygame.transform.flip(frame, True, False)
        frame = pygame.transform.scale_by(frame, self.scale)
        window.blit(frame, (self.x,self.y))

        self.advance_frame()

    def hover_check(self, mouse_x, mouse_y):
        self.hovered = self.obj.rect.collidepoint(mouse_x, mouse_y)
        return self.hovered
    
    def invert_x_axis(self):
        self.inverted = not(self.inverted)
    


    # def set_frame(self, frame): 
class circ():
    def __init__(self, rad, center):
        self.rad = rad
        self.center = center

class obj(object):

    def __init__(self, x, y, width, height, collide_method):
        valid = {"rect", "circle"}
        if collide_method not in valid:
            raise ValueError("results: status must be one of %r." % valid)
        
        self.collide_method = collide_method
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.update(x,y)

    def update(self, x, y):
        self.x = x
        self.y = y
        self.rad = self.width/2
        self.center = [self.x+(self.width/2), self.y+(self.height/2)]
        self.corner = [x+self.width, y+self.height]
        self.circle = circ(self.rad, self.center)
        self.rect = pygame.rect.Rect(x, y, self.width, self.height)

    def dimensions(self, w, h):
        self.rect = pygame.rect.Rect(self.x, self.y, w, h)
        self.width = w
        self.height = h    


    def asdict(self):
        return {"x": self.x, "y": self.y, "x_tamanho": self.larg, "y_tamanho": self.alt, "collide_method": self.collide_method}
    
class path_preview(object):
    def __init__(self, vet_dir, dist, g, pombo):
        self.balls = []
        qnt_balls = (int(dist*0.1)//5)+5
        vel = vet_dir*dist

        for _ in range(qnt_balls):
            ball = entidade(0,0,10,10,"rect","path_ball")
            self.balls.append(ball)
    
        for i in range(1,len(self.balls)):
            b = i+1
            pos = pombo
            for _ in range((30//qnt_balls)*b):
                vel += g
                pos += vel * 0.2
            self.balls[i].move(pos[0], pos[1])

        
    def blit(self, window):
        for ball in self.balls:
            ball.blit(window)
            
    
    
# teste = obj(1,2,2,3,"rect")
# print(teste.asdict()["x"])
# print(teste.rect.colliderect(teste))

    