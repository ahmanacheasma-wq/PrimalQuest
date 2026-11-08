
import pygame
import random


class Monster:
    def __init__(self):
        self.rect = pygame.Rect(300, 100, 50, 50)
        self.speed_x = 3
        self.speed_y = 2
        self.color = (230, 60, 60)

    def move(self, width, height):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.left <= 0 or self.rect.right >= width:
            self.speed_x = -self.speed_x

        if self.rect.top <= 0 or self.rect.bottom >= height:
            self.speed_y = -self.speed_y

    def reset_position(self, width, height):
        self.rect.x = random.randint(0, width - self.rect.width)
        self.rect.y = random.randint(50, 300)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
