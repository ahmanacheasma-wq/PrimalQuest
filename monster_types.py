import math
import random

from monster import Monster
from abilities import Shooter, Shielded


class NormalMonster(Monster):
    def __init__(self, x, y):
        super().__init__(x, y, max_health=3)


class FastMonster(Monster):
    def __init__(self, x, y):
        super().__init__(x, y, width=40, height=40, max_health=2,
                         speed_x=6, speed_y=4, color=(255, 140, 0))


class StrongMonster(Monster):
    def __init__(self, x, y):
        super().__init__(x, y, width=70, height=70, max_health=8,
                         speed_x=1, speed_y=1, color=(150, 30, 30),
                         damage_multipliers={"bullet": 0.5})


class FlyingMonster(Monster):
    """Vole en ligne ondulée, rebondit uniquement sur les côtés."""

    def __init__(self, x, y):
        super().__init__(x, y, width=45, height=30, max_health=3,
                         speed_x=4, speed_y=0, color=(160, 80, 255),
                         damage_multipliers={"laser": 2.0})
        self.base_y = y
        self._angle = 0.0

    def move(self, width, height):
        self.rect.x += self.speed_x
        if self.rect.left <= 0 or self.rect.right >= width:
            self.speed_x = -self.speed_x
        self._angle += 0.08
        self.rect.y = self.base_y + int(30 * math.sin(self._angle))


class ImmobileMonster(Monster):
    """Ne bouge jamais, mais respecte le contrat de move() (LSP)."""

    def __init__(self, x, y):
        super().__init__(x, y, width=55, height=55, max_health=5,
                         speed_x=0, speed_y=0, color=(90, 90, 90),
                         damage_multipliers={"laser": 0.5})

    def move(self, width, height):
        pass


class ShooterMonster(Monster, Shooter):
    def __init__(self, x, y):
        Monster.__init__(self, x, y, max_health=4, color=(200, 200, 60))
        self.setup_shooter(interval=120)


class ShieldedMonster(Shielded, Monster):
    def __init__(self, x, y):
        Monster.__init__(self, x, y, max_health=3, color=(60, 200, 200))
        self.setup_shield(shield=3)


MONSTER_TYPES = [
    NormalMonster,
    FastMonster,
    StrongMonster,
    FlyingMonster,
    ImmobileMonster,
    ShooterMonster,
    ShieldedMonster,
]


def create_random_monster(screen_width, screen_height):
    """Fabrique un monstre d'un type au hasard. Ajouter un type = l'ajouter à la liste (OCP)."""
    monster_class = random.choice(MONSTER_TYPES)
    x = random.randint(0, screen_width - 70)
    y = random.randint(50, 300)
    return monster_class(x, y)
