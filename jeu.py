import pygame
import sys
import math
from constantes import *
from plateau import init_plateau, appliquer_coup, lister_coups_valides
from algo_jeu import minmax
from interface import dessiner_plateau, ecran_fin


def menu(screen):
	"""
	Prend en entrée l'écran pygame
	---------------------------------------------------------------------------
	Affiche le menu principal avec les différents modes de jeu (2 joueurs, Joueur vs IA, IA vs IA).
	Gère les clics sur les boutons pour sélectionner le mode de jeu.
	---------------------------------------------------------------------------
	Retourne un tuple (mode, joueur_humain) selon le choix de l'utilisateur
	"""
	fond = pygame.image.load("background.jpg").convert_alpha()
	fond = pygame.transform.scale(fond, (840, 640))
	options = ["2 joueurs", "Joueur vs IA", "IA vs IA"]

	while True:
		screen.blit(fond, (0, 0))
		btns = [pygame.Rect(840 // 2 - 150, 200 + i * 100, 300, 60) for i in range(3)]
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
				if btns[0].collidepoint(event.pos):
					return "2J", None
				elif btns[1].collidepoint(event.pos):
					return choisir_couleur(screen)
				elif btns[2].collidepoint(event.pos):
					return "IAvsIA", None


def choisir_couleur(screen):
	"""
	Prend en entrée l'écran pygame
	---------------------------------------------------------------------------
	Affiche un menu pour choisir la couleur du joueur humain (Noirs ou Blancs) lors d'une partie contre l'IA.
	Gère les clics sur les boutons pour sélectionner la couleur.
	---------------------------------------------------------------------------
	Retourne un tuple ("IA", couleur) où couleur est 'N' ou 'B'
	"""
	fond = pygame.image.load("background.jpg").convert_alpha()
	fond = pygame.transform.scale(fond, (840, 640))
	options = ["Jouer Noirs", "Jouer Blancs"]
	
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
				if btns[0].collidepoint(event.pos):
					return "IA", 'N'
				elif btns[1].collidepoint(event.pos):
					return "IA", 'B'


def boucle_jeu(screen, mode, joueur_humain=None):
	"""
	Prend en entrée l'écran pygame, le mode de jeu et éventuellement la couleur du joueur humain
	---------------------------------------------------------------------------
	Gère la boucle principale du jeu : affichage du plateau, gestion des tours, application des coups,
	appel de l'IA si besoin, détection de la fin de partie et affichage de l'écran de fin.
	---------------------------------------------------------------------------
	Retourne None (fonction bloquante jusqu'à la fin de la partie ou retour au menu)
	"""
	plateau = init_plateau()
	joueur = 'N'
	IA_joueur = 'B' if joueur_humain == 'N' else 'N' if joueur_humain == 'B' else None
	clock = pygame.time.Clock()

	while True:
		coups = lister_coups_valides(plateau, joueur)
		maison_rect = dessiner_plateau(
			plateau, coups, screen, afficher_menu=(mode != "IAvsIA"), joueur=joueur
		)
		pygame.display.flip()

		# Vérifie la fin de partie (aucun coup possible pour les deux joueurs)
		if not coups:
			joueur = 'B' if joueur == 'N' else 'N'
			if not lister_coups_valides(plateau, joueur):
				noirs = sum(row.count('N') for row in plateau)
				blancs = sum(row.count('B') for row in plateau)
				if mode == "IA":
					resultat = "egalite" if noirs == blancs else None
					ecran_fin(screen, resultat, noirs, blancs, IA_joueur)
				elif mode == "IAvsIA":
					resultat = "noirs" if noirs > blancs else "blancs" if noirs < blancs else "egalite"
					ecran_fin(screen, resultat, noirs, blancs)
				else:
					resultat = "noirs" if noirs > blancs else "blancs" if noirs < blancs else "egalite"
					ecran_fin(screen, resultat, noirs, blancs)
				return

		# Tour de l'IA ou mode IA vs IA : l'IA joue automatiquement
		if (mode == "IA" and joueur == IA_joueur) or mode == "IAvsIA":
			_, coup = minmax(plateau, 5, True, joueur, -math.inf, math.inf, joueur)
			pygame.time.delay(500)
			if coup:
				appliquer_coup(plateau, *coup, joueur)
				joueur = 'B' if joueur == 'N' else 'N'
			continue

		# Gestion des événements pour le joueur humain
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if mode == "IAvsIA":
				continue
			elif event.type == pygame.MOUSEBUTTONDOWN:
				# Retour au menu si clic sur le bouton
				if maison_rect is not None and maison_rect.collidepoint(event.pos):
					return
				x, y = event.pos[1] // TAILLE_CASE, event.pos[0] // TAILLE_CASE
				if (x, y) in coups:
					appliquer_coup(plateau, x, y, joueur)
					joueur = 'B' if joueur == 'N' else 'N'

		clock.tick(FPS)
