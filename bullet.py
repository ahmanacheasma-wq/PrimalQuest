import math
import pygame

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800

WEAPONS = {
    "bullet": {"damage": 2, "color": (255, 230, 50)},
    "laser": {"damage": 2, "color": (0, 255, 255)},
    "enemy": {"damage": 1, "color": (255, 120, 0)},
}


class Bullet:
    def __init__(
        self,
        x,
        y,
        kind="bullet",
        direction=-1,
        dx=0.0
    ):
        weapon = WEAPONS[kind]

        self.kind = kind
        self.damage = weapon["damage"]
        self.color = weapon["color"]

        self.speed = 5 if kind == "enemy" else 10

        # Vérification des valeurs reçues
        values = (x, y, dx, direction)

        self.valid = all(
            math.isfinite(value)
            for value in values
        )

        if self.valid:
            self.x = float(x)
            self.y = float(y)
            self.dx = float(dx)
            self.dy = float(direction)
        else:
            # Projectile invalide : il ne sera pas affiché.
            self.x = 0.0
            self.y = 0.0
            self.dx = 0.0
            self.dy = 0.0

        # Forme adaptée à la direction
        if abs(self.dx) > abs(self.dy):
            width, height = 20, 10
        else:
            width, height = 10, 20

        self.rect = pygame.Rect(0, 0, width, height)

        self.rect.center = (
            round(self.x),
            round(self.y)
        )

    def move(self):
        if not self.valid:
            return

        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

        if not math.isfinite(self.x) or not math.isfinite(self.y):
            self.valid = False
            return

        self.rect.center = (
            round(self.x),
            round(self.y)
        )

    def is_off_screen(self):
        if not self.valid:
            return True

        return (
            self.rect.bottom < 0
            or self.rect.top > SCREEN_HEIGHT
            or self.rect.right < 0
            or self.rect.left > SCREEN_WIDTH
        )

    def draw(self, screen):
        if not self.valid:
            return

        pygame.draw.rect(
            screen,
            self.color,
            self.rect,
            border_radius=4
        )