
import pygame
from assets import Assets


class View:
    """Affiche le jeu : écran d'accueil et partie."""

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

        self.start_button_rect = pygame.Rect(0, 0, 260, 65)
        self.start_button_rect.center = (
            width // 2, height // 2 + 100
        )

        self.button_rect = pygame.Rect(0, 0, 260, 60)
        self.button_rect.center = (
            width // 2, height // 2 + 60
        )

    def draw_start_screen(self):
        self.draw_background(1)

        overlay = pygame.Surface(
            (self.width, self.height), pygame.SRCALPHA
        )
        overlay.fill((0, 0, 0, 155))
        self.screen.blit(overlay, (0, 0))

        title = self.big_font.render(
            "PRIMAL QUEST", True, (255, 220, 150)
        )
        self.screen.blit(
            title,
            title.get_rect(center=(self.width // 2, 190))
        )

        subtitle_font = pygame.font.Font(None, 34)
        subtitle = subtitle_font.render(
            "Prepare-toi pour l'aventure !",
            True,
            self.WHITE
        )
        self.screen.blit(
            subtitle,
            subtitle.get_rect(center=(self.width // 2, 270))
        )

        pygame.draw.rect(
            self.screen, (35, 130, 65),
            self.start_button_rect, border_radius=14
        )
        pygame.draw.rect(
            self.screen, (180, 230, 170),
            self.start_button_rect, width=3, border_radius=14
        )

        start_text = self.button_font.render(
            "START", True, self.WHITE
        )
        self.screen.blit(
            start_text,
            start_text.get_rect(center=self.start_button_rect.center)
        )

        pygame.display.flip()

    def draw_background(self, level=1):
        """Décor utilisé pour l'écran d'accueil."""

        if level == 1:
            name = "fonds/fond.jpg"
        elif level == 2:
            name = "fonds/fond_foret.png"
        else:
            name = "fonds/fond_desert.png"

        self.draw_world_background(name)

    def draw_world_background(self, background_path):
        """Affiche le décor choisi par l'Abstract Factory."""

        background = self.assets.image(
            background_path,
            (self.width, self.height)
        )

        if background is not None:
            self.screen.blit(background, (0, 0))
        else:
            self.screen.fill(self.BACKGROUND_COLOR)
            print("Background introuvable :", background_path)

    def draw_info_panel(self, score, health, game_over=False):
        score_text = self.font.render(
            f"Score : {score}", True, self.WHITE
        )
        health_text = self.font.render(
            f"Vie : {health}", True, self.WHITE
        )

        status = "GAME OVER" if game_over else "En cours"
        status_color = self.RED if game_over else (120, 230, 120)

        status_text = self.font.render(
            f"Statut : {status}", True, status_color
        )

        self.screen.blit(score_text, (10, 10))
        self.screen.blit(health_text, (10, 40))
        self.screen.blit(status_text, (10, 70))

    def draw_level_info(self, level, time_left):
        text = self.font.render(
            f"Niveau : {level}   Temps : {time_left}s",
            True,
            self.WHITE
        )
        self.screen.blit(text, (10, 105))

    def draw_level_transition(self, message):
        overlay = pygame.Surface(
            (self.width, self.height), pygame.SRCALPHA
        )
        overlay.fill((0, 0, 0, 170))
        self.screen.blit(overlay, (0, 0))

        title = self.big_font.render(
            message, True, self.WHITE
        )
        self.screen.blit(
            title,
            title.get_rect(
                center=(self.width // 2, self.height // 2)
            )
        )

    def draw_game_over(self):
        overlay = pygame.Surface(
            (self.width, self.height), pygame.SRCALPHA
        )
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        title = self.big_font.render(
            "GAME OVER", True, self.RED
        )
        self.screen.blit(
            title,
            title.get_rect(
                center=(self.width // 2, self.height // 2 - 40)
            )
        )

        pygame.draw.rect(
            self.screen, (60, 160, 60),
            self.button_rect, border_radius=10
        )

        label = self.button_font.render(
            "Rejouer", True, self.WHITE
        )
        self.screen.blit(
            label,
            label.get_rect(center=self.button_rect.center)
        )

    def draw_player(self, player):
        image = self.assets.image(
            "joueurs/joueur.png", player.rect.size
        )

        if image is not None:
            self.screen.blit(image, player.rect.topleft)
        else:
            pygame.draw.rect(
                self.screen, player.color, player.rect
            )

    def draw_monster(self, monster, health_bar):
        name = type(monster).__name__.lower()

        monster_images = {
            "fastmonster": "monstres/chasingmonster.png",
            "flyingmonster": "monstres/shootermonster.png",
            "strongmonster": "monstres/shieldedmonster.png",
            "shootermonster": "monstres/shootermonster.png",
            "shieldedmonster": "monstres/shieldedmonster.png",
            "chasingmonster": "monstres/chasingmonster.png"
        }

        image_path = monster_images.get(
            name, "monstres/chasingmonsterr.png"
        )

        image = self.assets.image(
            image_path, monster.rect.size
        )

        if image is not None:
            self.screen.blit(image, monster.rect.topleft)
        else:
            pygame.draw.rect(
                self.screen, monster.color, monster.rect
            )

        health_bar.draw(self.screen, monster)

    def draw_bullet(self, bullet):
        image = self.assets.image(
            f"balles/{bullet.kind}.png", bullet.rect.size
        )

        if image is not None:
            self.screen.blit(image, bullet.rect.topleft)
        else:
            pygame.draw.rect(
                self.screen, bullet.color, bullet.rect
            )
