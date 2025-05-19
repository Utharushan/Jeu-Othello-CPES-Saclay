import pygame
from constantes import *
from plateau import score


def dessiner_plateau(plateau, coups_possibles, screen, afficher_menu=True, joueur='N'):
    """
    Prend en entrée le plateau, la liste des coups possibles, l'écran pygame,
    un booléen pour afficher le bouton menu, et le joueur courant
    ---------------------------------------------------------------
    Affiche graphiquement le plateau de jeu, les pions, les coups possibles
    (points noirs ou blancs selon le joueur), les scores et éventuellement le bouton menu.
    ---------------------------------------------------------------
    Retourne le rectangle du bouton menu si affiché, sinon None
    """
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
                couleur_point = NOIR if joueur == 'N' else BLANC
                pygame.draw.circle(screen, couleur_point, rect.center, 5)

    noirs = sum(row.count('N') for row in plateau)
    blancs = sum(row.count('B') for row in plateau)
    pygame.draw.rect(screen, (50, 50, 50), (DIMENSION, 0, 200, DIMENSION))
    text_noirs = font.render(f"Noirs: {noirs}", True, BLANC)
    text_blancs = font.render(f"Blancs: {blancs}", True, BLANC)
    screen.blit(text_noirs, (DIMENSION + 20, 50))
    screen.blit(text_blancs, (DIMENSION + 20, 100))

    if afficher_menu:
        maison_rect = pygame.Rect(DIMENSION + 50, DIMENSION - 100, 100, 50)
        pygame.draw.rect(screen, GRIS, maison_rect)
        maison_texte = font.render("Menu", True, NOIR)
        screen.blit(maison_texte, (maison_rect.x + (maison_rect.width - maison_texte.get_width()) // 2,
                                   maison_rect.y + (maison_rect.height - maison_texte.get_height()) // 2))
        return maison_rect
    else:
        return None


def ecran_fin(screen, resultat, noirs, blancs, IA_joueur=None):
    """
    Prend en entrée l'écran pygame, le résultat de la partie, le score noirs, le score blancs,
    et éventuellement la couleur jouée par l'IA
    ---------------------------------------------------------------
    Affiche l'écran de fin de partie avec le score, le gagnant, et un bouton pour retourner au menu.
    Gère aussi les messages spécifiques en cas de partie contre l'IA.
    ---------------------------------------------------------------
    Retourne None (fonction bloquante jusqu'à action utilisateur)
    """
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
