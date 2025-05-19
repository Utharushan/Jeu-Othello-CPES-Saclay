from constantes import TAILLE, DIRECTIONS

def init_plateau():
	"""
	---------------------------------------------------------------------------
	Crée et initialise un plateau de jeu Othello avec les 4 pions centraux placés.
	---------------------------------------------------------------------------
	Retourne le plateau sous forme de liste de listes
	"""
	plateau = [[None for _ in range(TAILLE)] for _ in range(TAILLE)]
	plateau[3][3] = 'B'
	plateau[3][4] = 'N'
	plateau[4][3] = 'N'
	plateau[4][4] = 'B'
	return plateau


def coup_valide(plateau, x, y, joueur):
	"""
	Prend en entrée un plateau, les coordonnées x, y et le joueur courant
	---------------------------------------------------------------------------
	Vérifie si le coup proposé est valide pour le joueur (au moins un pion adverse capturé).
	---------------------------------------------------------------------------
	Retourne True si le coup est valide, False sinon
	"""
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
	"""
	Prend en entrée un plateau et le joueur courant
	---------------------------------------------------------------------------
	Liste tous les coups valides possibles pour le joueur sur le plateau donné.
	---------------------------------------------------------------------------
	Retourne une liste de tuples (x, y) correspondant aux coups valides
	"""
	return [(i, j) for i in range(TAILLE) for j in range(TAILLE) if coup_valide(plateau, i, j, joueur)]


def appliquer_coup(plateau, x, y, joueur):
	"""
	Prend en entrée un plateau, les coordonnées x, y et le joueur courant
	---------------------------------------------------------------------------
	Place le pion du joueur sur la case (x, y) et retourne les pions adverses capturés dans toutes les directions.
	---------------------------------------------------------------------------
	"""
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
	"""
	Prend en entrée un plateau
	---------------------------------------------------------------------------
	Compte le nombre de pions noirs et blancs sur le plateau et calcule la différence.
	---------------------------------------------------------------------------
	Retourne un entier : (nombre de pions noirs - nombre de pions blancs)
	"""
	noirs = sum(row.count('N') for row in plateau)
	blancs = sum(row.count('B') for row in plateau)
	return noirs - blancs
