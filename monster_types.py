import math
import random

from monster import Monster
from abilities import Shooter, Shielded


class NormalMonster(Monster, Shooter):
    def __init__(self, x, y):
        Monster.__init__(self, x, y, width=100, height=100, max_health=3)
        self.setup_shooter(interval=150)


class FastMonster(Monster, Shooter):
    def __init__(self, x, y):
        Monster.__init__(self, x, y, width=85, height=85, max_health=2,
                         speed_x=6, speed_y=4, color=(255, 140, 0))
        self.setup_shooter(interval=120)


class StrongMonster(Monster, Shooter):
    def __init__(self, x, y):
        Monster.__init__(self, x, y, width=140, height=140, max_health=8,
                         speed_x=1, speed_y=1, color=(150, 30, 30),
                         damage_multipliers={"bullet": 0.5})
        self.setup_shooter(interval=180)


class FlyingMonster(Monster):
    """Vole en ligne ondulée, rebondit uniquement sur les côtés. Ne tire pas."""

    def __init__(self, x, y):
        super().__init__(x, y, width=100, height=70, max_health=3,
                         speed_x=4, speed_y=0, color=(160, 80, 255),
                         damage_multipliers={"laser": 2.0})
        self.base_y = y
        self._angle = 0.0

    def move(self, area, target=None):
        self.rect.x += self.speed_x
        if self.rect.left <= area.left or self.rect.right >= area.right:
            self.speed_x = -self.speed_x
        self._angle += 0.08
        self.rect.y = self.base_y + int(30 * math.sin(self._angle))
        self.rect.clamp_ip(area)


class ImmobileMonster(Monster):
    """Ne bouge jamais, mais respecte le contrat de move() (LSP). Ne tire pas."""

    def __init__(self, x, y):
        super().__init__(x, y, width=120, height=120, max_health=5,
                         speed_x=0, speed_y=0, color=(90, 90, 90),
                         damage_multipliers={"laser": 0.5})

    def move(self, area, target=None):
        pass


class ShooterMonster(Monster, Shooter):
    def __init__(self, x, y):
        Monster.__init__(self, x, y, width=100, height=100, max_health=4,
                         color=(200, 200, 60))
        self.setup_shooter(interval=120)


class ShieldedMonster(Shielded, Monster, Shooter):
    def __init__(self, x, y):
        Monster.__init__(self, x, y, width=100, height=100, max_health=3,
                         color=(60, 200, 200))
        self.setup_shield(shield=3)
        self.setup_shooter(interval=120)


class ChasingMonster(Monster, Shooter):
    """Monstre rose qui poursuit le joueur en ligne droite et lui tire dessus."""

    def __init__(self, x, y):
        Monster.__init__(self, x, y, width=95, height=95, max_health=3,
                         speed_x=2, speed_y=2, color=(255, 80, 180))
        self.setup_shooter(interval=90)

    def move(self, area, target=None):
        if target is None:
            super().move(area)
            return

        if self.rect.centerx < target.rect.centerx:
            self.rect.x += self.speed_x
        elif self.rect.centerx > target.rect.centerx:
            self.rect.x -= self.speed_x

        if self.rect.centery < target.rect.centery:
            self.rect.y += self.speed_y
        elif self.rect.centery > target.rect.centery:
            self.rect.y -= self.speed_y

        self.rect.clamp_ip(area)


MONSTER_TYPES = [
    # NormalMonster,
    # FastMonster,
    # StrongMonster,
    # FlyingMonster,
    # ImmobileMonster,
    ShooterMonster,
    ShieldedMonster,
    ChasingMonster,
]


def create_random_monster(area):
    """Fabrique un monstre d'un type au hasard, sur le sol de la zone de jeu (area)."""
    monster_class = random.choice(MONSTER_TYPES)
    x = random.randint(area.left, area.right - 140)
    y = random.randint(area.top, area.bottom - 140)
    return monster_class(x, y)