
import pygame
import random


class Monster:
    def __init__(self):
        self.rect = pygame.Rect(300, 100, 50, 50)
        self.speed_x = 3
        self.speed_y = 2
        self.color = (230, 60, 60)


        self.max_health = 100
        self.health = self.max_health

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
        self.health = self.max_health

    
    def take_damage(self, damage):
        self.health -= damage

        if self.health < 0:
            self.health = 0
    

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class HealthBar:
    def __init__(self, monster):
        self.monster = monster
        self.width = 50
        self.height = 6

    def draw(self, screen):
        x = self.monster.rect.x
        y = self.monster.rect.y - 10

        background = pygame.Rect(
            x, y, self.width, self.height
        )
        pygame.draw.rect(screen, (200, 0, 0), background)

        ratio = self.monster.health / self.monster.max_health
        current_width = int(self.width * ratio)

        health_rect = pygame.Rect(
            x, y, current_width, self.height
        )
        pygame.draw.rect(screen, (0, 200, 0), health_rect)
