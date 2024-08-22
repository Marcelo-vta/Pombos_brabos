# Example file showing a basic pygame "game loop"
import pygame
from game import menu
from load_assets import load_assets
from character import load_animations, anim_db

"""# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()"""

if __name__ == '__main__':
    pygame.init()

    window = pygame.display.set_mode((1900, 1080), pygame.FULLSCREEN)
    load_animations()
    anim_db()

    jogo = menu(window)
    while True:
        jogo.loop()
