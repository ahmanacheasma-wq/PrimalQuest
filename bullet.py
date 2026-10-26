
import pygame


class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x - 5, y, 10, 20)
        self.speed = 8
        self.color = (255, 230, 50)

    def move(self):
        self.rect.y -= self.speed

    def is_off_screen(self):
        return self.rect.bottom < 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
