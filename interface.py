import pygame
from constantes import *
from plateau import score


def dessiner_plateau(plateau, coups_possibles, screen):
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

	noirs = sum(row.count('N') for row in plateau)
	blancs = sum(row.count('B') for row in plateau)
	pygame.draw.rect(screen, (50, 50, 50), (DIMENSION, 0, 200, DIMENSION))
	text_noirs = font.render(f"Noirs: {noirs}", True, BLANC)
	text_blancs = font.render(f"Blancs: {blancs}", True, BLANC)
	screen.blit(text_noirs, (DIMENSION + 20, 50))
	screen.blit(text_blancs, (DIMENSION + 20, 100))

	maison_rect = pygame.Rect(DIMENSION + 50, DIMENSION - 100, 100, 50)
	pygame.draw.rect(screen, GRIS, maison_rect)
	maison_texte = font.render("Menu", True, NOIR)
	screen.blit(maison_texte, (maison_rect.x + (maison_rect.width - maison_texte.get_width()) // 2,
							   maison_rect.y + (maison_rect.height - maison_texte.get_height()) // 2))
	return maison_rect


def ecran_fin(screen, resultat, noirs, blancs, IA_joueur=None):
	screen.fill(NOIR)

	texte_score = f"Score - Noirs: {noirs}, Blancs: {blancs}"
	font_fin = pygame.font.SysFont(None, 64)
	texte_surface_score = font_fin.render(texte_score, True, BLANC)
	screen.blit(texte_surface_score, (840 // 2 - texte_surface_score.get_width() // 2, 640 // 2 - texte_surface_score.get_height() // 2 - 100))

	if resultat == "noirs":
		texte = "Victoire des Noirs !"
	elif resultat == "blancs":
		texte = "Victoire des Blancs !"
	elif resultat == "egalite":
		texte = "Égalité !"

	if IA_joueur == 'N':
		texte = "Défaite contre l'IA (Noirs) !" if noirs > blancs else "Victoire contre l'IA (Noirs) !"
	elif IA_joueur == 'B':
		texte = "Défaite contre l'IA (Blancs) !" if blancs > noirs else "Victoire contre l'IA (Blancs) !"


	texte_surface = font_fin.render(texte, True, BLANC)
	screen.blit(texte_surface, (840 // 2 - texte_surface.get_width() // 2, 640 // 2 - texte_surface.get_height() // 2))

	btn_menu = pygame.Rect(840 // 2 - 100, 640 // 2 + 50, 200, 60)
	pygame.draw.rect(screen, GRIS, btn_menu)
	texte_menu = font.render("Menu", True, NOIR)
	screen.blit(texte_menu, (btn_menu.x + (btn_menu.width - texte_menu.get_width()) // 2,
							 btn_menu.y + (btn_menu.height - texte_menu.get_height()) // 2))

	pygame.display.flip()

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if btn_menu.collidepoint(event.pos):
					return
			elif event.type == pygame.KEYDOWN:
				return
