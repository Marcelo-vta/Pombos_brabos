import pygame
import sys

class Instrucoes():
    def init(self, window):

        pygame.init()

        self.clock = pygame.time.Clock()
        
        self.titulo = 'Instruções'
        self.explicacao = """Neste jogo, o objetivo é atingir a pessoa com o projétil do pombo, nas 3 fases. Você tem 3 tentativas por fase.
Dica: Tome cuidado ao voar muito próximo do sol...
        

  Como jogar:
        
 - Pressione com o botão esquerdo do mouse e puxe para qualquer direção, e então, ao soltar o botão do mouse, o pombo será lançado.
 - Para soltar um projétil, clique novamente com o botão esquerdo enquanto o pombo estiver no ar.
 - Após o pouso do pombo aguarde alguns segundos, ele retornará à posição inicial.
 - O sol possui efeitos na trajetória do pombo, leve isso em consideração em seus lançamentos.

 
  Divirta-se. :)
    """
        self.tela = pygame.Rect(window.get_size()[0]/6, window.get_size()[1]/6, 4*window.get_size()[0]/6, 4*window.get_size()[1]/6)
        self.fechar = pygame.Rect(self.tela.x + self.tela.width - 43, self.tela.y, 43, 40)
        self.window = window

        self.fonte_bot = pygame.font.Font(pygame.font.get_default_font(), 16)
        self.fonte_tit = pygame.font.Font(pygame.font.get_default_font(), 20)
        self.fonte_txt = pygame.font.Font(pygame.font.get_default_font(), 14)

    def divide_texto(self, fonte):
        words = self.explicacao.split(' ')
        space = fonte.size(' ')[0]
        max_width = self.tela.width - 30
        linha, linhas = [], []
        tam_linha = 0

        for i in range(len(words)):
            if '\n' in words[i]:
                sp = words[i].split('\n')
                if words[i] in linha:
                    linhas += [' '.join(linha[:-1] + [sp[0]])]
                else:
                    linhas += [' '.join(linha + [sp[0]])]
                linha = [sp[1]]
                tam_linha = fonte.render(sp[1], True, (255, 255, 255)).get_width()
                continue
            
            if tam_linha > max_width:
                linhas += [' '.join(linha[:-1])]
                linha = [linha[-1]]
                tam_linha = fonte.render(linha[-1], True, (255, 255, 255)).get_width()
                continue

            if i == len(words)-1:
                tam_linha += fonte.render(words[i], True, (255, 255, 255)).get_width() + space
                linha += [words[i]]
                linhas += [' '.join(linha)]
                continue

            tam_linha += fonte.render(words[i], True, (255, 255, 255)).get_width() + space
            linha += [words[i]]

        return linhas
    
    def loop(self, state):
        mbd = False
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mbd = True

        if self.fechar.collidepoint(mouse_x, mouse_y):
            if mbd:
                return "stage1"

        #desenha base da tela de instruções
        pygame.draw.rect(self.window, (0,0,0), self.tela)

        #desenha botão de fechar
        pygame.draw.rect(self.window, (0,0,0), self.fechar)
        pygame.draw.rect(self.window, (255,255,255), self.fechar, width=1)

        x = self.fonte_bot.render('x', True, (255, 255, 255))
        self.window.blit(x, (self.fechar.x + self.fechar.width/2 - x.get_width()/2, self.fechar.y + self.fechar.height/2 - x.get_height()/2))

        #desenha título da página atual
        palavra = self.fonte_tit.render(self.titulo, True, (255, 255, 255))
        self.window.blit(palavra, (self.tela.x + 20, self.tela.y + 70))

        #desenha instruções de jogo da página atual
        j = 0
        for linha in self.divide_texto(self.fonte_txt):
            self.window.blit(self.fonte_txt.render(linha, True, (255, 255, 255)), (self.tela.x + 20, self.tela.y + 110 + 18*j))
            j += 1        
        
        pygame.display.update()
        self.clock.tick(60)
        return "pass"