import pygame

def load_assets(window):
    assets = {

    }
    for i in  range(1,10):
        for j in range(1,8):
            assets[f"p_{i}_{j}"] = pygame.image.load(f"Pombos_brabos/assets/Pombos/p_{i}_{j}.jpeg")
    
    background = pygame.image.load(r"Pombos_brabos\assets\Title_Image_Day.png")
    assets["background"] = pygame.transform.scale(background, window.get_size())

    title = pygame.image.load(r"Pombos_brabos\assets\titulo.png")
    assets["title"] = pygame.transform.scale_by(title, 1.75)

    play_btn = pygame.image.load(r"Pombos_brabos\assets\Jogar1.png")
    assets["play_bt"] = pygame.transform.scale_by(title, 1.75)

    play_btn_clk = pygame.image.load(r"Pombos_brabos\assets\Jogar2.png")
    assets["play_bt_c"] = pygame.transform.scale_by(title, 1.75)

    return assets

