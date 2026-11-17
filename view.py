import pygame


class View:
    """Affiche le jeu. Ne contient aucune règle de jeu (MVC)."""

    WHITE = (255, 255, 255)
    RED = (255, 80, 80)

    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 90)
        self.button_font = pygame.font.Font(None, 42)
        self.button_rect = pygame.Rect(0, 0, 260, 60)
        self.button_rect.center = (width // 2, height // 2 + 60)

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