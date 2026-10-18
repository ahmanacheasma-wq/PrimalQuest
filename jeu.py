import pygame
import random

pygame.init()

# ---------- Constantes ----------
LARGEUR = 800
HAUTEUR = 600
VITESSE_JOUEUR = 5
VITESSE_BALLE = 8

# ---------- Fenêtre ----------
ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("jeu de tir")
horloge = pygame.time.Clock()
zone_de_jeu = ecran.get_rect()

# ---------- Objets du jeu ----------
joueur = pygame.Rect(380, 520, 40, 40)
monstre = pygame.Rect(300, 100, 50, 50)
balle = None                      # None = pas de balle à l'écran

# vitesse du monstre (x et y)
vitesse_monstre_x = 3
vitesse_monstre_y = 2

score = 0
police = pygame.font.Font(None, 36)
jeu_actif = True

# ---------- Boucle principale ----------
while jeu_actif:

    # 1) Événements (actions ponctuelles)
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            jeu_actif = False

        if evenement.type == pygame.KEYDOWN:
            if evenement.key == pygame.K_ESCAPE:
                jeu_actif = False
            # tir : seulement s'il n'y a pas déjà une balle
            if evenement.key == pygame.K_SPACE and balle is None:
                balle = pygame.Rect(joueur.centerx - 5, joueur.top, 10, 20)

    # 2) Entrées continues (touches maintenues)
    touches = pygame.key.get_pressed()
    if touches[pygame.K_LEFT]:
        joueur.x -= VITESSE_JOUEUR
    if touches[pygame.K_RIGHT]:
        joueur.x += VITESSE_JOUEUR
    if touches[pygame.K_UP]:
        joueur.y -= VITESSE_JOUEUR
    if touches[pygame.K_DOWN]:
        joueur.y += VITESSE_JOUEUR

    # le joueur reste dans la zone de jeu
    joueur.clamp_ip(zone_de_jeu)

    # 3) Mise à jour : monstre
    monstre.x += vitesse_monstre_x
    monstre.y += vitesse_monstre_y

    # rebond sur les bords
    if monstre.left <= 0 or monstre.right >= LARGEUR:
        vitesse_monstre_x = -vitesse_monstre_x
    if monstre.top <= 0 or monstre.bottom >= HAUTEUR:
        vitesse_monstre_y = -vitesse_monstre_y

    # 3) Mise à jour : balle
    if balle is not None:
        balle.y -= VITESSE_BALLE

        if balle.colliderect(monstre):
            score += 1
            balle = None
            monstre.x = random.randint(0, LARGEUR - 50)
            monstre.y = random.randint(50, 300)

        elif balle.bottom < 0:    # la balle sort par le haut
            balle = None

    # 4) Rendu
    ecran.fill((25, 25, 40))
    pygame.draw.rect(ecran, (50, 150, 255), joueur)
    pygame.draw.rect(ecran, (230, 60, 60), monstre)

    if balle is not None:
        pygame.draw.rect(ecran, (255, 230, 50), balle)

    texte = police.render(f"Score : {score}", True, (255, 255, 255))
    ecran.blit(texte, (10, 10))

    pygame.display.flip()
    horloge.tick(60)

pygame.quit()