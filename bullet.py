import pygame

SCREEN_HEIGHT = 600

WEAPONS = {
    "bullet": {"damage": 2, "color": (255, 230, 50)},
    "laser": {"damage": 2, "color": (0, 255, 255)},
    "enemy": {"damage": 1, "color": (255, 120, 0)},
}


class Bullet:
    def __init__(self, x, y, kind="bullet", direction=-1):
        weapon = WEAPONS[kind]
        self.kind = kind
        self.damage = weapon["damage"]
        self.color = weapon["color"]
        self.direction = direction
        self.speed = 8
        self.rect = pygame.Rect(x - 5, y, 10, 20)

    def move(self):
        self.rect.y += self.speed * self.direction

    def is_off_screen(self):
        return self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
