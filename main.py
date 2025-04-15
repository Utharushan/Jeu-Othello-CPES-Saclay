import pygame
import sys
import copy
import math

# Constantes
TAILLE = 8
TAILLE_CASE = 80
DIMENSION = TAILLE * TAILLE_CASE
FPS = 60
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
VERT = (0, 128, 0)
GRIS = (192, 192, 192)

pygame.init()
font = pygame.font.SysFont(None, 32)

# Initialisation écran
screen = pygame.display.set_mode((DIMENSION + 200, DIMENSION))
pygame.display.set_caption("Othello")

# Directions possibles (8)
DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1),
			  (0, -1),          (0, 1),
			  (1, -1),  (1, 0),  (1, 1)]


def init_plateau():
	plateau = [[None for _ in range(TAILLE)] for _ in range(TAILLE)]
	plateau[3][3] = 'B'
	plateau[3][4] = 'N'
	plateau[4][3] = 'N'
	plateau[4][4] = 'B'
	return plateau


def dessiner_plateau(plateau, coups_possibles):
	screen.fill(VERT)
	for x in range(TAILLE):
		for y in range(TAILLE):
			rect = pygame.Rect(y * TAILLE_CASE, x * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE)
			pygame.draw.rect(screen, NOIR, rect, 1)
			if plateau[x][y] == 'N':
				pygame.draw.circle(screen, NOIR, rect.center, TAILLE_CASE // 2 - 5)
			elif plateau[x][y] == 'B':
				pygame.draw.circle(screen, BLANC, rect.center, TAILLE_CASE // 2 - 5)
			elif (x, y) in coups_possibles:
				pygame.draw.circle(screen, GRIS, rect.center, 5)

	# Affichage scores
	noirs = sum(row.count('N') for row in plateau)
	blancs = sum(row.count('B') for row in plateau)
	pygame.draw.rect(screen, (50, 50, 50), (DIMENSION, 0, 200, DIMENSION))
	text_noirs = font.render(f"Noirs: {noirs}", True, BLANC)
	text_blancs = font.render(f"Blancs: {blancs}", True, BLANC)
	screen.blit(text_noirs, (DIMENSION + 20, 50))
	screen.blit(text_blancs, (DIMENSION + 20, 100))

	# Bouton maison
	maison_rect = pygame.Rect(DIMENSION + 50, DIMENSION - 100, 100, 50)
	pygame.draw.rect(screen, GRIS, maison_rect)
	maison_texte = font.render("Menu", True, NOIR)
	screen.blit(maison_texte, (maison_rect.x + (maison_rect.width - maison_texte.get_width()) // 2,
							   maison_rect.y + (maison_rect.height - maison_texte.get_height()) // 2))
	return maison_rect


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
			eval, _ = minmax(p_copy, profondeur-1, False, 'B' if joueur == 'N' else 'N', alpha, beta)
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
			eval, _ = minmax(p_copy, profondeur-1, True, 'B' if joueur == 'N' else 'N', alpha, beta)
			if eval < min_eval:
				min_eval = eval
				meilleur_coup = coup
			beta = min(beta, eval)
			if beta <= alpha:
				break
		return min_eval, meilleur_coup


def menu():
    # Chargement de l'image de fond
    fond = pygame.image.load("background.jpg").convert_alpha()
    fond = pygame.transform.scale(fond, (840, 640))

    running = True
    choix = 0
    options = ["2 joueurs", "Joueur vs IA"]
    while running:
        screen.blit(fond, (0, 0))

        # Création des boutons
        btn1 = pygame.Rect(840 // 2 - 150, 200, 300, 60)
        btn2 = pygame.Rect(840 // 2 - 150, 300, 300, 60)
        pygame.draw.rect(screen, GRIS, btn1)
        pygame.draw.rect(screen, GRIS, btn2)

        # Affichage des textes centrés dans les boutons
        txt1 = font.render("2 joueurs", True, NOIR)
        txt2 = font.render("Joueur vs IA", True, NOIR)
        screen.blit(txt1, (btn1.x + (btn1.width - txt1.get_width()) // 2, btn1.y + (btn1.height - txt1.get_height()) // 2))
        screen.blit(txt2, (btn2.x + (btn2.width - txt2.get_width()) // 2, btn2.y + (btn2.height - txt2.get_height()) // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if btn1.collidepoint(event.pos):
                    return "2J"
                elif btn2.collidepoint(event.pos):
                    return "IA"


def boucle_jeu(mode):
	plateau = init_plateau()
	joueur = 'N'
	IA_joueur = 'B' if mode == "IA" else None
	clock = pygame.time.Clock()

	while True:
		coups = lister_coups_valides(plateau, joueur)
		maison_rect = dessiner_plateau(plateau, coups)
		pygame.display.flip()

		if not coups:
			joueur = 'B' if joueur == 'N' else 'N'
			if not lister_coups_valides(plateau, joueur):
				break
			continue

		if mode == "IA" and joueur == IA_joueur:
			_, coup = minmax(plateau, 3, True, joueur, -math.inf, math.inf)
			pygame.time.delay(500)
			if coup:
				appliquer_coup(plateau, *coup, joueur)
				joueur = 'B' if joueur == 'N' else 'N'
			continue

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if maison_rect.collidepoint(event.pos):
					return
				x, y = event.pos[1] // TAILLE_CASE, event.pos[0] // TAILLE_CASE
				if (x, y) in coups:
					appliquer_coup(plateau, x, y, joueur)
					joueur = 'B' if joueur == 'N' else 'N'

		clock.tick(FPS)

	# Affichage fin de jeu
	dessiner_plateau(plateau, [])
	pygame.display.flip()
	pygame.time.wait(3000)


if __name__ == '__main__':
	while True:
		choix = menu()
		boucle_jeu(choix)
