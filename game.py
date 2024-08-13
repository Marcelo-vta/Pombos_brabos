import pygame

def inicializa():
    """
    Inicializa todas as informações e objetos do jogo.
    """

    pygame.init()

    config = ""

    asset = {
        **config.asset,
        'def_font' : pygame.font.Font(pygame.font.get_default_font(), 15),
        'leg_font' : pygame.font.Font(pygame.font.get_default_font(), 11),
        'money_font' : pygame.font.Font(pygame.font.match_font('Abel'), 30),
        'old_font' : pygame.font.Font(pygame.font.match_font('Old English Five'), 45),
        'objs' : {},
        'personagens' : {},
    }

    window = pygame.display.set_mode(tuple(asset['tam_tela']), vsync=asset['vsync'], flags=pygame.SCALED)
    pygame.display.set_caption('Casino Nights')

    state = {
        'tela_jogo' : 'inicio',
        'aviso' : None,
        'jogador' : asset['jogador'].pos,
        'vel' : [0,0],
        'last_updated' : 0,
        'dinheiro' : 2000,
        'dt' : 0,
        'minigame' : None,
    }

    return window, asset, state


def atualiza_estado(window, asset, state):
    """
    Atualiza estado do jogo, e checa ações e interações.
    """
    if state['tela_jogo'] != 'game_over':
        t_atual = pygame.time.get_ticks()
        state['dt'] = (t_atual - state['last_updated'])/1000
        state['last_updated'] = t_atual

    pygame.mixer.music.set_volume(asset['vol_musica'])
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load('musica/jazz_fundo.mp3')
        pygame.mixer.music.play(-1, fade_ms=1500)
        
    return True

def game_loop(window, asset, state):
    """
    Loop principal do jogo, onde roda todas as outras funções necessárias.
    """
    game = True

    while game:
        game = atualiza_estado(window, asset, state)
        pass
        pygame.display.update()