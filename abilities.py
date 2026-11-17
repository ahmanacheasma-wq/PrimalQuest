import math

from bullet import Bullet


class Shooter:
    """Capacité (ISP) : tire périodiquement une balle vers le joueur."""

    def setup_shooter(self, interval):
        self.shoot_interval = interval
        self._shoot_timer = interval

    def try_shoot(self, target=None):
        self._shoot_timer -= 1
        if self._shoot_timer > 0:
            return None
        self._shoot_timer = self.shoot_interval

        origin_x = self.rect.centerx
        origin_y = self.rect.bottom
        if target is None:
            return Bullet(origin_x, origin_y, kind="enemy", direction=1)

        dx = target.rect.centerx - origin_x
        dy = target.rect.centery - origin_y
        length = math.hypot(dx, dy) or 1
        return Bullet(origin_x, origin_y, kind="enemy",
                      direction=dy / length, dx=dx / length)


class Shielded:
    """
    Capacité (ISP) : un bouclier absorbe les dégâts avant la vie.
    Doit être placée AVANT Monster dans l'héritage pour que son
    _apply_damage soit appelé en premier.
    """

    def setup_shield(self, shield):
        self.shield = shield

    def _apply_damage(self, amount):
        absorbed = min(self.shield, amount)
        self.shield -= absorbed
        remaining = amount - absorbed
        if remaining > 0:
            super()._apply_damage(remaining)