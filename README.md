# Jeu Othello

Ce projet est une implémentation complète du jeu **Othello (Reversi)** en Python, avec une interface graphique développée avec **Pygame**. Il propose un mode "2 joueurs" ainsi qu’un mode "Joueur contre IA" utilisant l’algorithme **Minimax avec élagage alpha-bêta**.

---

## Fonctionnalités

### Modes de jeu

- **Deux joueurs** : Deux joueurs humains peuvent jouer en local.
- **Joueur vs IA** :
  - Le joueur peut choisir de jouer les noirs ou les blancs.
  - L’IA utilise une stratégie de recherche basée sur l’algorithme Minimax optimisé.

### Intelligence Artificielle

- **Algorithme Minimax** avec élagage alpha-bêta pour limiter l’espace de recherche.
- **Fonction d’évaluation personnalisée** basée sur :
  - Une table de pondération des positions (valeur stratégique des cases).
  - La mobilité (réduction des coups disponibles pour l’adversaire).
- **Tri des coups** pour maximiser l’efficacité de la recherche.

### Interface graphique

- Affichage interactif du plateau.
- Visualisation des scores en temps réel.
- Écran de fin indiquant le gagnant et les scores finaux.
- Retours visuels dynamiques pour une meilleure jouabilité.

---

## Prérequis

- Python 3.8 ou supérieur
- Bibliothèque [Pygame](https://www.pygame.org/)

### Installation des dépendances

```bash
pip install pygame
```

---

## Règles du jeu

### Objectif

Avoir **plus de pions de votre couleur** que l’adversaire à la fin de la partie.

### Déroulement

- Les joueurs jouent à tour de rôle.
- À chaque tour, le joueur doit **poser un pion de manière à encadrer un ou plusieurs pions adverses** entre le pion posé et un autre pion de la même couleur.
- Les pions encadrés sont retournés.
- Si un joueur ne peut pas jouer, il passe son tour.

### Fin de la partie

La partie se termine lorsque plus aucun coup n’est possible pour les deux joueurs. Le joueur avec le plus de pions sur le plateau gagne.

---

## Structure du projet

```
.
├── main.py              # Point d’entrée du programme
├── jeu.py               # Logique du déroulement d'une partie
├── interface.py         # Interface graphique avec Pygame
├── algo_jeu.py          # IA : Minimax et fonctions d’évaluation
├── plateau.py           # Fonctions de gestion du plateau
├── constantes.py        # Paramètres (couleurs, dimensions, etc.)
├── README.md            # Documentation du projet
```
