# Example file showing a basic pygame "game loop"
import pygame
from game import menu, fase1
from load_assets import load_assets
from character import load_animations, anim_db
from instrucoes import Instrucoes


if __name__ == '__main__':
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
                game = menu()
                game.init(window, state)
                loop = "pass"
            if loop == "stage1":
                game = fase1()
                game.init(window, state)
                loop = "pass"
            if loop == 'instrucoes':
                game = Instrucoes()
                game.init(window)
                loop = "pass"
        else:
            loop = game.loop(state)
