import pygame

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800

WEAPONS = {
    "bullet": {"damage": 2, "color": (255, 230, 50)},
    "laser": {"damage": 2, "color": (0, 255, 255)},
    "enemy": {"damage": 1, "color": (255, 120, 0)},
}


class Bullet:
    def __init__(self, x, y, kind="bullet", direction=-1, dx=0.0):
        weapon = WEAPONS[kind]
        self.kind = kind
        self.damage = weapon["damage"]
        self.color = weapon["color"]
        self.dx = dx           # déplacement horizontal (0 = tout droit)
        self.dy = direction    # déplacement vertical
        self.speed = 8
        self.x = float(x - 5)
        self.y = float(y)
        self.rect = pygame.Rect(int(self.x), int(self.y), 10, 20)

    def move(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def is_off_screen(self):
        return (self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT
                or self.rect.right < 0 or self.rect.left > SCREEN_WIDTH)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)