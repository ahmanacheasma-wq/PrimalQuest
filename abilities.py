from bullet import Bullet


class Shooter:
    """Capacité (ISP) : tire périodiquement une balle vers le bas."""

    def setup_shooter(self, interval):
        self.shoot_interval = interval
        self._shoot_timer = interval

    def try_shoot(self):
        self._shoot_timer -= 1
        if self._shoot_timer > 0:
            return None
        self._shoot_timer = self.shoot_interval
        return Bullet(self.rect.centerx, self.rect.bottom, kind="enemy", direction=1)


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
