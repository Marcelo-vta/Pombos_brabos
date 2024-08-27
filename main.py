# Example file showing a basic pygame "game loop"
import pygame
from pag_menu import Menu
from character import load_animations, anim_db
from instrucoes import Instrucoes
from fase1 import Fase1
from fase2 import Fase2
from end import end

def main():
    pygame.init()

    # window = pygame.display.set_mode((1900, 1080), pygame.FULLSCREEN)
    # window = pygame.display.set_mode((1280,720), pygame.FULLSCREEN)
    window = pygame.display.set_mode((1280,720))
    load_animations()
    anim_db()

    state = {}

    loop = "menu"
    while True:
        if loop != "pass":        
            if loop == "menu":
                game = Menu()
                game.init(window, state)
                loop = "pass"
            if loop == "stage1":
                game = Fase1()
                game.init(window, state)
                loop = "pass"
            if loop == "stage2":
                game = Fase2()
                game.init(window, state)
                loop = "pass"
            if loop == 'instrucoes':
                game = Instrucoes()
                game.init(window)
                loop = "pass"
            if loop == 'end':
                game = end()
                game.init(window,state)
                loop = "pass"

        else:
            loop = game.loop(state)