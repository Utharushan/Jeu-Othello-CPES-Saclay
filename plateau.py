from constantes import TAILLE, DIRECTIONS

def init_plateau():
	plateau = [[None for _ in range(TAILLE)] for _ in range(TAILLE)]
	plateau[3][3] = 'B'
	plateau[3][4] = 'N'
	plateau[4][3] = 'N'
	plateau[4][4] = 'B'
	return plateau


def coup_valide(plateau, x, y, joueur):
	if plateau[x][y] is not None:
		return False
	adv = 'B' if joueur == 'N' else 'N'
	for dx, dy in DIRECTIONS:
		i, j = x + dx, y + dy
		trouve_adv = False
		while 0 <= i < TAILLE and 0 <= j < TAILLE and plateau[i][j] == adv:
			i += dx
			j += dy
			trouve_adv = True
		if trouve_adv and 0 <= i < TAILLE and 0 <= j < TAILLE and plateau[i][j] == joueur:
			return True
	return False


def lister_coups_valides(plateau, joueur):
	return [(i, j) for i in range(TAILLE) for j in range(TAILLE) if coup_valide(plateau, i, j, joueur)]


def appliquer_coup(plateau, x, y, joueur):
	plateau[x][y] = joueur
	adv = 'B' if joueur == 'N' else 'N'
	for dx, dy in DIRECTIONS:
		i, j = x + dx, y + dy
		a_retourner = []
		while 0 <= i < TAILLE and 0 <= j < TAILLE and plateau[i][j] == adv:
			a_retourner.append((i, j))
			i += dx
			j += dy
		if 0 <= i < TAILLE and 0 <= j < TAILLE and plateau[i][j] == joueur:
			for (ix, iy) in a_retourner:
				plateau[ix][iy] = joueur


def score(plateau):
	noirs = sum(row.count('N') for row in plateau)
	blancs = sum(row.count('B') for row in plateau)
	return noirs - blancs
