import pygame


class HealthBar:
    """Affiche la barre de vie d'un monstre. Ne modifie pas le monstre (SRP)."""

    def __init__(self, height=5, offset=8):
        self.height = height
        self.offset = offset
        self.background_color = (80, 0, 0)
        self.foreground_color = (0, 220, 0)

    def draw(self, screen, monster):
        ratio = monster.health / monster.max_health
        width = monster.rect.width
        y = monster.rect.top - self.offset
        background = pygame.Rect(monster.rect.left, y, width, self.height)
        foreground = pygame.Rect(monster.rect.left, y, int(width * ratio), self.height)
        pygame.draw.rect(screen, self.background_color, background)
        pygame.draw.rect(screen, self.foreground_color, foreground)
