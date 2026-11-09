import pygame
from player import Player
from monster_types import create_random_monster
from abilities import Shooter
from health_bar import HealthBar
from bullet import Bullet


class GameBoard:
    def __init__(self):
        pygame.init()

        self.width = 800
        self.height = 600

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("PrimalQuest")

        self.clock = pygame.time.Clock()
        self.game_area = self.screen.get_rect()

        self.health_bar = HealthBar()
        self.weapons = ["bullet", "laser"]

        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 90)
        self.button_font = pygame.font.Font(None, 42)
        self.button_rect = pygame.Rect(0, 0, 260, 60)
        self.button_rect.center = (self.width // 2, self.height // 2 + 60)

        self.running = True
        self.reset()

    def reset(self):
        """Remet la partie à zéro (utilisé au démarrage et après un game over)."""
        self.player = Player()
        self.monsters = [create_random_monster(self.width, self.height) for _ in range(2)]
        self.bullets = []          # tirs du joueur
        self.enemy_bullets = []    # tirs des monstres
        self.weapon_index = 0
        self.score = 0

    @property
    def weapon(self):
        return self.weapons[self.weapon_index]

    @property
    def game_over(self):
        return not self.player.is_alive

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

                if event.key == pygame.K_TAB and not self.game_over:
                    self.weapon_index = (self.weapon_index + 1) % len(self.weapons)

                if event.key == pygame.K_SPACE and not self.game_over:
                    self.bullets.append(Bullet(
                        self.player.rect.centerx,
                        self.player.rect.top,
                        kind=self.weapon,
                        direction=-1,
                    ))

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.game_over and self.button_rect.collidepoint(event.pos):
                    self.reset()

    def update(self):
        keys = pygame.key.get_pressed()
        self.player.move(keys, self.game_area)
        self._update_monsters()
        self._update_player_bullets()
        self._update_enemy_bullets()

    def _update_monsters(self):
        for monster in self.monsters:
            monster.move(self.width, self.height, self.player)
            if isinstance(monster, Shooter):
                shot = monster.try_shoot(self.player)
                if shot is not None:
                    self.enemy_bullets.append(shot)

    def _update_player_bullets(self):
        for bullet in list(self.bullets):
            bullet.move()
            target = self._find_target(bullet)
            if target is not None:
                target.take_damage(bullet)
                self.bullets.remove(bullet)
                if not target.is_alive:
                    self.score += 1
                    self._replace_monster(target)
            elif bullet.is_off_screen():
                self.bullets.remove(bullet)

    def _find_target(self, bullet):
        for monster in self.monsters:
            if monster.is_alive and bullet.rect.colliderect(monster.rect):
                return monster
        return None

    def _replace_monster(self, dead):
        self.monsters.remove(dead)
        self.monsters.append(create_random_monster(self.width, self.height))

    def _update_enemy_bullets(self):
        for bullet in list(self.enemy_bullets):
            bullet.move()
            if bullet.rect.colliderect(self.player.rect):
                self.player.take_damage(bullet.damage)
                self.enemy_bullets.remove(bullet)
            elif bullet.is_off_screen():
                self.enemy_bullets.remove(bullet)

    def draw(self):
        self.screen.fill((25, 25, 40))

        self.player.draw(self.screen)

        for monster in self.monsters:
            monster.draw(self.screen)
            self.health_bar.draw(self.screen, monster)

        for bullet in self.bullets + self.enemy_bullets:
            bullet.draw(self.screen)

        self._draw_hud()

        if self.game_over:
            self._draw_game_over()

        pygame.display.flip()

    def _draw_hud(self):
        score_text = self.font.render(f"Score : {self.score}", True, (255, 255, 255))
        health_text = self.font.render(f"Vie : {self.player.health}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(health_text, (10, 40))

    def _draw_game_over(self):
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        title = self.big_font.render("GAME OVER", True, (255, 80, 80))
        self.screen.blit(title, title.get_rect(center=(self.width // 2, self.height // 2 - 40)))

        pygame.draw.rect(self.screen, (60, 160, 60), self.button_rect, border_radius=10)
        label = self.button_font.render("Rejouer", True, (255, 255, 255))
        self.screen.blit(label, label.get_rect(center=self.button_rect.center))

    def run(self):
        while self.running:
            self.handle_events()
            if not self.game_over:
                self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()