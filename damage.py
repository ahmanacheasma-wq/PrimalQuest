import math
from abc import ABC, abstractmethod


class DamageCalculator(ABC):
    """Abstraction : calcule les dégâts infligés par une attaque à une cible (DIP)."""

    @abstractmethod
    def compute(self, attack, target):
        ...


class MultiplierDamageCalculator(DamageCalculator):
    """
    Multiplie les dégâts selon le type d'attaque (attack.kind).
    multiplicateur < 1 : résistance, multiplicateur > 1 : faiblesse.
    """

    def compute(self, attack, target):
        multiplier = target.damage_multipliers.get(attack.kind, 1.0)
        return math.ceil(attack.damage * multiplier)
