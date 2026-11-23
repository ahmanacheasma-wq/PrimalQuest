import random
import pygame
from damage import MultiplierDamageCalculator


class Monster:
    """
    Monstre de base : gère sa vie, ses déplacements et son corps.
    N'affiche pas sa barre de vie (SRP) et ne connaît pas le type d'arme (DIP).
    """

    def __init__(self, x, y, width=50, height=50, max_health=3,
                 speed_x=3, speed_y=2, color=(230, 60, 60),
                 damage_multipliers=None, damage_calculator=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.max_health = max_health
        self.health = max_health
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.color = color
        self.damage_multipliers = damage_multipliers or {}
        self.damage_calculator = damage_calculator or MultiplierDamageCalculator()

    @property
    def is_alive(self):
        return self.health > 0

    def take_damage(self, attack):
        amount = self.damage_calculator.compute(attack, self)
        if amount > 0:
            self._apply_damage(amount)
        return amount

    def _apply_damage(self, amount):
        self.health = max(0, self.health - amount)

    def move(self, area, target=None):
        """Rebondit sur les bords de la zone de jeu (area) et y reste."""
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.left <= area.left or self.rect.right >= area.right:
            self.speed_x = -self.speed_x

        if self.rect.top <= area.top or self.rect.bottom >= area.bottom:
            self.speed_y = -self.speed_y

        self.rect.clamp_ip(area)

    def reset_position(self, area):
        self.rect.x = random.randint(area.left, area.right - self.rect.width)
        self.rect.y = random.randint(area.top, area.bottom - self.rect.height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)