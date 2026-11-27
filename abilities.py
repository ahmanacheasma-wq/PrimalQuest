import math
from bullet import Bullet


class Shooter:
    """Capacité permettant au monstre de tirer vers le joueur."""

    def setup_shooter(self, interval):
        self.base_shoot_interval = interval
        self.shoot_interval = interval
        self._shoot_timer = interval

    def set_shoot_interval(self, interval):
        """Modifie la fréquence de tir selon le niveau."""
        self.shoot_interval = max(18, int(interval))
        self._shoot_timer = min(
            self._shoot_timer,
            self.shoot_interval
        )

    def try_shoot(self, target=None):
        self._shoot_timer -= 1

        if self._shoot_timer > 0:
            return None

        self._shoot_timer = self.shoot_interval

        if target is None:
            return Bullet(
                self.rect.centerx,
                self.rect.bottom + 5,
                kind="enemy",
                direction=1
            )

        # Coordonnées du monstre et du joueur
        monster_x = self.rect.centerx
        monster_y = self.rect.centery

        player_x = target.rect.centerx
        player_y = target.rect.centery

        values = (monster_x, monster_y, player_x, player_y)

        if not all(math.isfinite(value) for value in values):
            return None

        # Calcul de la direction vers le joueur
        dx = player_x - monster_x
        dy = player_y - monster_y

        length = math.hypot(dx, dy)

        if not math.isfinite(length) or length < 0.0001:
            return None

        ux = dx / length
        uy = dy / length

        if not math.isfinite(ux) or not math.isfinite(uy):
            return None

        # Position de départ du projectile
        half_width = self.rect.width / 2
        half_height = self.rect.height / 2

        distance_x = (
            half_width / abs(ux)
            if abs(ux) > 0.0001
            else float("inf")
        )

        distance_y = (
            half_height / abs(uy)
            if abs(uy) > 0.0001
            else float("inf")
        )

        distance = min(distance_x, distance_y) + 8

        origin_x = monster_x + ux * distance
        origin_y = monster_y + uy * distance

        if not all(math.isfinite(value) for value in (
            origin_x, origin_y, ux, uy
        )):
            return None

        return Bullet(
            origin_x,
            origin_y,
            kind="enemy",
            direction=uy,
            dx=ux
        )


class Shielded:
    """Le bouclier absorbe les dégâts avant la vie."""

    def setup_shield(self, shield):
        self.shield = shield

    def _apply_damage(self, amount):
        absorbed = min(self.shield, amount)
        self.shield -= absorbed

        remaining = amount - absorbed

        if remaining > 0:
            super()._apply_damage(remaining)