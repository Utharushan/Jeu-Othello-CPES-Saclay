import pygame
from constantes import DIMENSION
from jeu import menu, boucle_jeu

screen = pygame.display.set_mode((DIMENSION + 200, DIMENSION))
pygame.display.set_caption("Othello")

if __name__ == '__main__':
	while True:
		choix = menu(screen)
		boucle_jeu(screen, choix)
