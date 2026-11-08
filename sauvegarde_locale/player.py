
import pygame


class Player:
    def __init__(self):
        self.rect = pygame.Rect(380, 520, 40, 40)
        self.speed = 5
        self.color = (50, 150, 255)

    def move(self, keys, game_area):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        self.rect.clamp_ip(game_area)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
