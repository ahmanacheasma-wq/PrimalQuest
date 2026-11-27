
import math
import random

from monster import Monster
from abilities import Shooter, Shielded


class NormalMonster(Monster, Shooter):
    def __init__(self, x, y):
        Monster.__init__(
            self,
            x, y,
            width=100,
            height=100,
            max_health=3
        )
        self.setup_shooter(interval=100)


class FastMonster(Monster, Shooter):
    """Monstre rapide du désert."""

    def __init__(self, x, y):
        Monster.__init__(
            self,
            x, y,
            width=85,
            height=85,
            max_health=2,
            speed_x=6,
            speed_y=4,
            color=(255, 140, 0)
        )
        self.setup_shooter(interval=65)


class StrongMonster(Monster, Shooter):
    """Monstre puissant du désert."""

    def __init__(self, x, y):
        Monster.__init__(
            self,
            x, y,
            width=140,
            height=140,
            max_health=8,
            speed_x=2,
            speed_y=2,
            color=(150, 30, 30),
            damage_multipliers={"bullet": 0.5}
        )
        self.setup_shooter(interval=85)


class FlyingMonster(Monster, Shooter):
    """Monstre volant qui tire vers le joueur."""

    def __init__(self, x, y):
        Monster.__init__(
            self,
            x, y,
            width=100,
            height=70,
            max_health=3,
            speed_x=4,
            speed_y=0,
            color=(160, 80, 255),
            damage_multipliers={"laser": 2.0}
        )

        self.base_y = y
        self._angle = 0.0
        self.setup_shooter(interval=75)

    def move(self, area, target=None):
        self.rect.x += self.speed_x

        if self.rect.left <= area.left:
            self.rect.left = area.left
            self.speed_x = abs(self.speed_x)

        elif self.rect.right >= area.right:
            self.rect.right = area.right
            self.speed_x = -abs(self.speed_x)

        self._angle += 0.08
        self.rect.y = self.base_y + int(
            30 * math.sin(self._angle)
        )

        self.rect.clamp_ip(area)


class ImmobileMonster(Monster):
    """Monstre immobile."""

    def __init__(self, x, y):
        super().__init__(
            x, y,
            width=120,
            height=120,
            max_health=5,
            speed_x=0,
            speed_y=0,
            color=(90, 90, 90),
            damage_multipliers={"laser": 0.5}
        )

    def move(self, area, target=None):
        pass


class ShooterMonster(Monster, Shooter):
    def __init__(self, x, y):
        Monster.__init__(
            self,
            x, y,
            width=120,
            height=120,
            max_health=4,
            color=(200, 200, 60)
        )
        self.setup_shooter(interval=85)


class ShieldedMonster(Shielded, Monster, Shooter):
    def __init__(self, x, y):
        Monster.__init__(
            self,
            x, y,
            width=120,
            height=120,
            max_health=3,
            color=(60, 200, 200)
        )
        self.setup_shield(shield=3)
        self.setup_shooter(interval=90)


class ChasingMonster(Monster, Shooter):
    """Monstre qui poursuit le joueur et lui tire dessus."""

    def __init__(self, x, y):
        Monster.__init__(
            self,
            x, y,
            width=95,
            height=95,
            max_health=3,
            speed_x=1,
            speed_y=1,
            color=(255, 80, 180)
        )
        self.setup_shooter(interval=80)

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
    ShooterMonster,
    ShieldedMonster,
    ChasingMonster,
]


class MonsterFactory:
    """Factory Method."""

    def create_monster(self, x, y):
        raise NotImplementedError


class ShooterMonsterFactory(MonsterFactory):
    def create_monster(self, x, y):
        return ShooterMonster(x, y)


class ShieldedMonsterFactory(MonsterFactory):
    def create_monster(self, x, y):
        return ShieldedMonster(x, y)


class ChasingMonsterFactory(MonsterFactory):
    def create_monster(self, x, y):
        return ChasingMonster(x, y)


class RandomMonsterFactory(MonsterFactory):
    def __init__(self):
        self.factories = [
            ShooterMonsterFactory(),
            ShieldedMonsterFactory(),
            ChasingMonsterFactory(),
        ]

    def create_monster(self, x, y):
        factory = random.choice(self.factories)
        return factory.create_monster(x, y)


def create_random_monster(area):
    x = random.randint(
        area.left,
        area.right - 140
    )

    y = random.randint(
        area.top,
        area.bottom - 140
    )

    factory = RandomMonsterFactory()
    return factory.create_monster(x, y)
