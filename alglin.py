import numpy as np
from consts import const_G

def vetor_direcao(pos_inicial, pos_final):
    """
    Direção do vetor entre pos_inicial (normalmente posição do personagem) e pos_final (normalmente direção do mouse).

    Retorna: Vetor normalizado
    """
    v = pos_final - pos_inicial
    return np.array((1/np.linalg.norm(v)) * v)


def dist(pos_corpo, pos_personagem):
    """
    A distância deve ser calculada com as posições do centro de cada corpo.
    """
    return np.sqrt((pos_corpo[0] - pos_personagem[0])*2 + (pos_corpo[1] - pos_personagem[1])*2)


def forca_g(pos_corpo, pos_personagem, m_corpo, m_personagem):
    return const_G * m_corpo * m_personagem / dist(pos_corpo, pos_personagem)**2


def acc_gravitacional(pos_corpo, pos_personagem, m_corpo, m_personagem):
    """
    Aceleração do corpo é a força entre os corpos dividido pela massa do corpo sendo acelerado.

    Retorna:
    [Aceleração do personagem, Aceleração do corpo]
    """
    f = forca_g(pos_corpo, pos_personagem, m_corpo, m_personagem)
    return f/m_personagem, f/m_corpo

def deformacao_elastica(massa_personagem, acc_personagem, k):
    """
    Deformação elástica é a aceleração do personagem dividida pela constante elástica.

    - acc_personagem deve ser do tipo np.array ou int/float.

    Retorna:
    Deformação elástica
    """
    return acc_personagem*massa_personagem/k

def acc_elastica(massa_personagem, acc_personagem, k):
    """
    Aceleração do corpo é a força entre os corpos dividido pela massa do corpo sendo acelerado.

    Retorna:
    Aceleração do personagem
    """

    return k*deformacao_elastica(massa_personagem, acc_personagem, k)/massa_personagem


def vetor_aceleracao(pos_inicial, pos_final, acc):
    """
    Aceleração do personagem é a aceleração multiplicada pela direção do vetor entre pos_inicial e pos_final.

    Retorna:
    Vetor aceleração
    """
    return acc * vetor_direcao(pos_inicial, pos_final)