import pygame
from assets import Assets


class View:
    """Affiche le jeu. Ne contient aucune règle de jeu (MVC)."""

    WHITE = (255, 255, 255)
    RED = (255, 80, 80)
    BACKGROUND_COLOR = (25, 25, 40)

    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.assets = Assets()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 90)
        self.button_font = pygame.font.Font(None, 42)
        self.button_rect = pygame.Rect(0, 0, 260, 60)
        self.button_rect.center = (width // 2, height // 2 + 60)

    def draw_background(self):
        background = self.assets.image("fonds/fond.png", (self.width, self.height))
        if background is not None:
            self.screen.blit(background, (0, 0))
        else:
            self.screen.fill(self.BACKGROUND_COLOR)

    def draw_info_panel(self, score, health):
        score_text = self.font.render(f"Score : {score}", True, self.WHITE)
        health_text = self.font.render(f"Vie : {health}", True, self.WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(health_text, (10, 40))

    def draw_game_over(self):
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        title = self.big_font.render("GAME OVER", True, self.RED)
        self.screen.blit(title, title.get_rect(center=(self.width // 2, self.height // 2 - 40)))

        pygame.draw.rect(self.screen, (60, 160, 60), self.button_rect, border_radius=10)
        label = self.button_font.render("Rejouer", True, self.WHITE)
        self.screen.blit(label, label.get_rect(center=self.button_rect.center))

    def draw_player(self, player):
        image = self.assets.image("joueurs/joueur.png", player.rect.size)
        if image is not None:
            self.screen.blit(image, player.rect.topleft)
        else:
            pygame.draw.rect(self.screen, player.color, player.rect)

    def draw_monster(self, monster, health_bar):
        name = type(monster).__name__.lower()
        image = self.assets.image(f"monstres/{name}.png", monster.rect.size)
        if image is not None:
            self.screen.blit(image, monster.rect.topleft)
        else:
            pygame.draw.rect(self.screen, monster.color, monster.rect)
        health_bar.draw(self.screen, monster)

    def draw_bullet(self, bullet):
        image = self.assets.image(f"balles/{bullet.kind}.png", bullet.rect.size)
        if image is not None:
            self.screen.blit(image, bullet.rect.topleft)
        else:
            pygame.draw.rect(self.screen, bullet.color, bullet.rect)