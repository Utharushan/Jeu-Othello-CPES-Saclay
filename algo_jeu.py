import copy
import math
from plateau import appliquer_coup, lister_coups_valides, score


def minmax(plateau, profondeur, maximisant, joueur, alpha, beta):
	coups = lister_coups_valides(plateau, joueur)
	if profondeur == 0 or not coups:
		return score(plateau), None

	meilleur_coup = None
	if maximisant:
		max_eval = -math.inf
		for coup in coups:
			p_copy = copy.deepcopy(plateau)
			appliquer_coup(p_copy, *coup, joueur)
			eval, _ = minmax(p_copy, profondeur - 1, False, 'B' if joueur == 'N' else 'N', alpha, beta)
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
			eval, _ = minmax(p_copy, profondeur - 1, True, 'B' if joueur == 'N' else 'N', alpha, beta)
			if eval < min_eval:
				min_eval = eval
				meilleur_coup = coup
			beta = min(beta, eval)
			if beta <= alpha:
				break
		return min_eval, meilleur_coup
