import pygame

# -----------------------------------------------------------------------------------------------------------------------
#                                                 V papo de animação V

animation_db = {}

def load_animations():
    assets_path = "assets/"

    global animation_db 
    
    with open(assets_path+"animations.txt") as r:
        animations = r.read().split("\n")
    
    for i in range(len(animations)):
        animations[i] = animations[i].split(" ")

    for inf in animations:
        e_type = inf[0].split("/")[0]
        frames = [int(i) for i in inf[1].split(";")]
        state = inf[0].split('/')[1]
        endcode = inf[4]
        scale = inf[3]

        if e_type not in animation_db:
            animation_db[e_type] = {}
        if e_type == "pombo":
            state = inf[0].split('/')[2]
            for i in range(1,10):
                if str(i) not in animation_db[e_type]:
                    animation_db[e_type][str(i)] = {}
                animation_db[e_type][str(i)][state] = []
                for j in range(len(frames)):
                    for _ in range(1, frames[j]+1):
                        sprite = pygame.image.load(f"{assets_path}{e_type}/{str(i)}/{state}/{str(j+1)}{endcode}")
                        sprite = pygame.transform.scale_by(sprite, float(scale))
                        animation_db[e_type][str(i)][state].append(sprite)
        else:
            animation_db[e_type][inf[0].split("/")[1]] = []
            for j in range(len(frames)):
                for _ in range(1, frames[j]+1):
                    sprite = pygame.image.load(f"{assets_path}{e_type}/{state}/{str(j+1)}{endcode}")
                    pygame.transform.scale_by(sprite, float(scale))
                    animation_db[e_type][state].append(sprite)

def anim_db():
    return animation_db

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
    def __init__(self, x, y, width, height, collide_method, e_type):

        valid = {"rect", "circle"}
        if collide_method not in valid:
            raise ValueError("results: status must be one of %r." % valid)

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.collide_method = collide_method

        self.type = e_type

        self.rotation = 0
        self.state = 0
        self.collide_list = []
        self.obj = obj(x, y, self.width, self.height, collide_method)

        self.action = "idle"
        self.frame = 0
        self.set_action("idle")
        self.skin = 1

        pass

    def find_sequence(self):
        global animation_db

        busca = animation_db[self.type]
        if self.type == "pombo":
            busca = busca[str(self.skin)]

        return busca[self.action]
    
    def set_frame(self, new_frame):
        self.frame = new_frame % len(self.find_sequence())
    
    def advance_frame(self):
        self.frame += 1
        if self.frame >= len(self.find_sequence()):
            self.frame = 0

    def change_skin(self, new_skin):
        if self.type == "pombo" and new_skin in range(1,10):
            self.skin = new_skin
    
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
        window.blit(sequence[self.frame], (self.x,self.y))
        self.advance_frame()
    


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
        self.rad = self.width/2
        self.center = [self.x+(self.width/2), self.y+(self.height/2)]
        self.corner = [x+self.width, y+self.height]
        self.circle = circ(self.rad, self.center)
        self.rect = pygame.Rect(x, y, self.width, self.height)        


    def asdict(self):
        return {"x": self.x, "y": self.y, "x_tamanho": self.larg, "y_tamanho": self.alt, "collide_method": self.collide_method}
    
# teste = obj(1,2,2,3,"rect")
# print(teste.asdict()["x"])
# print(teste.rect.colliderect(teste))

    