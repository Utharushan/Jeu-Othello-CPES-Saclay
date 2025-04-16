import copy
import math
from plateau import appliquer_coup, lister_coups_valides, score

COEFF_POSITION = [
    [100, -20, 10, 5, 5, 10, -20, 100],
    [-20, -50, -2, -2, -2, -2, -50, -20],
    [10, -2, -1, -1, -1, -1, -2, 10],
    [5, -2, -1, -1, -1, -1, -2, 5],
    [5, -2, -1, -1, -1, -1, -2, 5],
    [10, -2, -1, -1, -1, -1, -2, 10],
    [-20, -50, -2, -2, -2, -2, -50, -20],
    [100, -20, 10, 5, 5, 10, -20, 100]
]

def eval_simple(plateau, joueur):
    adv = 'B' if joueur == 'N' else 'N'
    s = score(plateau)
    diff = s if joueur == 'N' else -s

    poids = 0
    for i in range(8):
        for j in range(8):
            if plateau[i][j] == joueur:
                poids += COEFF_POSITION[i][j]
            elif plateau[i][j] == adv:
                poids -= COEFF_POSITION[i][j]
    return diff + poids

def eval_mobilite(plateau, joueur):
    adv = 'B' if joueur == 'N' else 'N'
    coups = lister_coups_valides(plateau, adv)
    return -len(coups)

def score_coup(coup, plateau, joueur, IA_joueur):
    i, j = coup
    s = COEFF_POSITION[i][j]
    p_copy = copy.deepcopy(plateau)
    appliquer_coup(p_copy, i, j, joueur)
    val = eval_simple(p_copy, IA_joueur)
    val += eval_mobilite(p_copy, IA_joueur)
    return val

def trier_coups(coups, plateau, joueur, maximisant, IA_joueur):
    n = len(coups)
    scores = [score_coup(c, plateau, joueur, IA_joueur) for c in coups]

    for i in range(n):
        for j in range(i + 1, n):
            if (maximisant and scores[j] > scores[i]) or (not maximisant and scores[j] < scores[i]):
                scores[i], scores[j] = scores[j], scores[i]
                coups[i], coups[j] = coups[j], coups[i]

    return coups

def minmax(plateau, profondeur, maximisant, joueur, alpha, beta, IA_joueur):
    coups = lister_coups_valides(plateau, joueur)
    if profondeur == 0 or not coups:
        return eval_simple(plateau, IA_joueur), None

    coups = trier_coups(coups, plateau, joueur, maximisant, IA_joueur)
    meilleur_coup = None

    if maximisant:
        max_eval = -math.inf
        for coup in coups:
            p_copy = copy.deepcopy(plateau)
            appliquer_coup(p_copy, *coup, joueur)
            eval, _ = minmax(p_copy, profondeur - 1, False, 'B' if joueur == 'N' else 'N', alpha, beta, IA_joueur)
            if eval > max_eval:
                max_eval = eval
                meilleur_coup = coup
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, meilleur_coup
    else:
        min_eval = math.inf
        for coup in coups:
            p_copy = copy.deepcopy(plateau)
            appliquer_coup(p_copy, *coup, joueur)
            eval, _ = minmax(p_copy, profondeur - 1, True, 'B' if joueur == 'N' else 'N', alpha, beta, IA_joueur)
            if eval < min_eval:
                min_eval = eval
                meilleur_coup = coup
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, meilleur_coup
