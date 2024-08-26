import numpy as np
from consts import const_G

def vetor_direcao(pos_inicial, pos_final = None):
    """
    Direção do vetor entre pos_inicial (normalmente posição do personagem) e pos_final (normalmente direção do mouse).

    Retorna: Vetor normalizado
    """
    try:
        v = pos_final - pos_inicial if pos_final.any() != None else pos_inicial
    except AttributeError:
        v = pos_final - pos_inicial if pos_final != None else pos_inicial
    return np.array((1/np.linalg.norm(v)) * v)


def calcula_angulo(vetor):
    """
    Calcula ângulo entre o eixo x e o vetor.

    Retorna: Ângulo em radianos.
    """
    vec_x = np.array([1, 0])
    return np.arccos((vetor_direcao(vetor) @ vec_x))


def dist(pos_corpo, pos_personagem):
    """
    A distância deve ser calculada com as posições do centro de cada corpo.
    """
    return ((pos_corpo[0] - pos_personagem[0])**2 + (pos_corpo[1] - pos_personagem[1])**2)**0.5


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

def acc_elastica(v_personagem, rot_trampolim):
    """
    Aceleração do corpo é a força entre os corpos dividido pela massa do corpo sendo acelerado.

    Retorna:
    Aceleração do personagem
    """
    if rot_trampolim == 'x':
        return v_personagem * np.array([-1.0, 0])
    elif rot_trampolim == 'y':
        return v_personagem * np.array([1.0, -1.0])


def vetor_aceleracao(pos_inicial, pos_final, acc):
    """
    Aceleração do personagem é a aceleração multiplicada pela direção do vetor entre pos_inicial e pos_final.

    Retorna:
    Vetor aceleração
    """
    return acc * vetor_direcao(pos_inicial, pos_final)