# PrimalQuest
# PrimalQuest

Jeu de tir 2D en Python avec Pygame, réalisé dans le cadre du TP2 (POO) du Master 1 GSI.

## Description

Le joueur contrôle un carré bleu et doit éliminer des monstres en tirant. Chaque monstre a sa propre vie, son propre comportement et parfois une capacité :

- **Monstre normal** : se déplace et rebondit sur les bords.
- **Monstre rapide** : plus rapide, moins de vie.
- **Monstre fort** : plus de vie, résiste aux balles.
- **Monstre volant** : vole en ligne ondulée, très vulnérable au laser.
- **Monstre immobile** : ne bouge pas, résiste au laser.
- **Monstre tireur** : tire périodiquement.
- **Monstre bouclier** : un bouclier absorbe les premiers dégâts.
- **Monstre rose** : poursuit le joueur et lui tire dessus.

Le joueur a 3 vies. Quand elles sont épuisées, la partie s'arrête sur l'écran GAME OVER, avec un bouton pour rejouer.

## Installation

Il faut Python 3 et Pygame :

```bash
pip install pygame
```

## Lancer le jeu

```bash
python main.py
```

## Commandes

| Touche | Action |
|---|---|
| Flèches | Déplacer le joueur |
| Espace | Tirer |
| TAB | Changer d'arme (balle ou laser) |
| ECHAP | Quitter |

## Structure du projet

- `main.py` : point d'entrée du jeu.
- `game_board.py` : boucle de jeu, collisions, score, affichage.
- `player.py` : le joueur (position, vie).
- `monster.py` : classe de base des monstres (vie, déplacement).
- `monster_types.py` : les différents types de monstres.
- `abilities.py` : capacités (tir, bouclier) utilisées par les monstres.
- `bullet.py` : balles du joueur et des monstres.
- `damage.py` : calcul des dégâts selon le type d'attaque.
- `health_bar.py` : barre de vie des monstres.