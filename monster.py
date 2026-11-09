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

    def move(self, width, height):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.left <= 0 or self.rect.right >= width:
            self.speed_x = -self.speed_x

        if self.rect.top <= 0 or self.rect.bottom >= height:
            self.speed_y = -self.speed_y

    def reset_position(self, width, height):
        self.rect.x = random.randint(0, width - self.rect.width)
        self.rect.y = random.randint(50, 300)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
