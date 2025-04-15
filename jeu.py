import pygame
import sys
import math
from constantes import *
from plateau import init_plateau, appliquer_coup, lister_coups_valides
from algo_jeu import minmax
from interface import dessiner_plateau, ecran_fin


def menu(screen):
	fond = pygame.image.load("background.jpg").convert_alpha()
	fond = pygame.transform.scale(fond, (840, 640))
	options = ["2 joueurs", "Joueur vs IA"]

	while True:
		screen.blit(fond, (0, 0))
		btns = [pygame.Rect(840 // 2 - 150, 200 + i * 100, 300, 60) for i in range(2)]
		for i, btn in enumerate(btns):
			pygame.draw.rect(screen, GRIS, btn)
			txt = font.render(options[i], True, NOIR)
			screen.blit(txt, (btn.x + (btn.width - txt.get_width()) // 2, btn.y + (btn.height - txt.get_height()) // 2))
		pygame.display.flip()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if btns[0].collidepoint(event.pos): return "2J"
				elif btns[1].collidepoint(event.pos): return "IA"


def boucle_jeu(screen, mode):
	plateau = init_plateau()
	joueur = 'N'
	IA_joueur = 'B' if mode == "IA" else None
	clock = pygame.time.Clock()

	while True:
		coups = lister_coups_valides(plateau, joueur)
		maison_rect = dessiner_plateau(plateau, coups, screen)
		pygame.display.flip()

		if not coups:
			joueur = 'B' if joueur == 'N' else 'N'
			if not lister_coups_valides(plateau, joueur):
				noirs = sum(row.count('N') for row in plateau)
				blancs = sum(row.count('B') for row in plateau)
				if mode == "IA":
					ecran_fin(screen, "victoire" if noirs > blancs else "defaite" if noirs < blancs else "egalite")
				else:
					ecran_fin(screen, "noirs" if noirs > blancs else "blancs" if noirs < blancs else "egalite")
				return
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
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if maison_rect.collidepoint(event.pos): return
				x, y = event.pos[1] // TAILLE_CASE, event.pos[0] // TAILLE_CASE
				if (x, y) in coups:
					appliquer_coup(plateau, x, y, joueur)
					joueur = 'B' if joueur == 'N' else 'N'

		clock.tick(FPS)
