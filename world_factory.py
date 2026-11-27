
import random
from abc import ABC, abstractmethod

from monster_types import (
    ShooterMonster,
    ShieldedMonster,
    ChasingMonster,
    FastMonster,
    FlyingMonster,
    StrongMonster
)


class WorldFactory(ABC):
    """Abstract Factory : crée une famille d'objets pour un monde."""

    @abstractmethod
    def create_background(self):
        pass

    @abstractmethod
    def create_monsters(self, area, count):
        pass

    @abstractmethod
    def create_weapons(self):
        pass

    @abstractmethod
    def create_reward(self):
        pass

    def random_position(self, area, monster_class):
        sizes = {
            ShooterMonster: (120, 120),
            ShieldedMonster: (120, 120),
            ChasingMonster: (95, 95),
            FastMonster: (85, 85),
            FlyingMonster: (100, 70),
            StrongMonster: (140, 140)
        }

        width, height = sizes.get(monster_class, (100, 100))

        x = random.randint(area.left, area.right - width)
        y = random.randint(area.top, area.bottom - height)

        return x, y

    def _create_monsters(self, area, count, monster_types):
        monsters = []

        for _ in range(count):
            monster_class = random.choice(monster_types)
            x, y = self.random_position(area, monster_class)
            monsters.append(monster_class(x, y))

        return monsters


class CaveWorldFactory(WorldFactory):
    """Famille d'objets du monde grotte."""

    def create_background(self):
        return "fonds/fond.jpg"

    def create_monsters(self, area, count):
        return self._create_monsters(
            area,
            count,
            [
                ShooterMonster,
                ShieldedMonster,
                ChasingMonster
            ]
        )

    def create_weapons(self):
        return ["bullet", "laser"]

    def create_reward(self):
        return {
            "name": "Relique ancienne",
            "health_bonus": 1,
            "score_bonus": 5
        }


class ForestWorldFactory(WorldFactory):
    """Famille d'objets du monde forêt."""

    def create_background(self):
        return "fonds/fond_foret.png"

    def create_monsters(self, area, count):
        return self._create_monsters(
            area,
            count,
            [
                ShooterMonster,
                ShieldedMonster,
                ChasingMonster
            ]
        )

    def create_weapons(self):
        return ["bullet", "laser"]

    def create_reward(self):
        return {
            "name": "Fruit sauvage",
            "health_bonus": 2,
            "score_bonus": 10
        }


class DesertWorldFactory(WorldFactory):
    """Famille d'objets du monde désert."""

    def create_background(self):
        return "fonds/fond_desert.png"

    def create_monsters(self, area, count):
        return self._create_monsters(
            area,
            count,
            [
                FastMonster,
                FlyingMonster,
                StrongMonster
            ]
        )

    def create_weapons(self):
        return ["bullet", "laser"]

    def create_reward(self):
        return {
            "name": "Cristal du désert",
            "health_bonus": 3,
            "score_bonus": 20
        }
