import pygame

TAILLE = 8
TAILLE_CASE = 80
DIMENSION = TAILLE * TAILLE_CASE
FPS = 60

NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
VERT = (0, 128, 0)
GRIS = (192, 192, 192)

DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1),
			  (0, -1),          (0, 1),
			  (1, -1), (1, 0),  (1, 1)]

pygame.init()
font = pygame.font.SysFont(None, 32)
