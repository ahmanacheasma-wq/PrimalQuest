
import pygame
from player import Player
from monster import Monster
from bullet import Bullet


class GameBoard:
    def __init__(self):
        pygame.init()

        self.width = 800
        self.height = 600

        self.screen = pygame.display.set_mode(
            (self.width, self.height)
        )
        pygame.display.set_caption("PrimalQuest")

        self.clock = pygame.time.Clock()
        self.game_area = self.screen.get_rect()

        self.player = Player()
        self.monster = Monster()
        self.bullet = None

        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

                if event.key == pygame.K_SPACE and self.bullet is None:
                    self.bullet = Bullet(
                        self.player.rect.centerx,
                        self.player.rect.top
                    )

    def update(self):
        keys = pygame.key.get_pressed()

        self.player.move(keys, self.game_area)
        self.monster.move(self.width, self.height)

        if self.bullet is not None:
            self.bullet.move()

            if self.bullet.rect.colliderect(self.monster.rect):
                self.score += 1
                self.bullet = None
                self.monster.reset_position(
                    self.width, self.height
                )

            elif self.bullet.is_off_screen():
                self.bullet = None

    def draw(self):
        self.screen.fill((25, 25, 40))

        self.player.draw(self.screen)
        self.monster.draw(self.screen)

        if self.bullet is not None:
            self.bullet.draw(self.screen)

        text = self.font.render(
            f"Score : {self.score}",
            True,
            (255, 255, 255)
        )
        self.screen.blit(text, (10, 10))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()
