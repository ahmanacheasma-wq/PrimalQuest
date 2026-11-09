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

        self.player = Player()
        self.monsters = [create_random_monster(self.width, self.height) for _ in range(2)]
        self.health_bar = HealthBar()

        self.bullets = []          # tirs du joueur
        self.enemy_bullets = []    # tirs des monstres
        self.weapons = ["bullet", "laser"]
        self.weapon_index = 0

        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.running = True

    @property
    def weapon(self):
        return self.weapons[self.weapon_index]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

                if event.key == pygame.K_TAB:
                    self.weapon_index = (self.weapon_index + 1) % len(self.weapons)

                if event.key == pygame.K_SPACE:
                    self.bullets.append(Bullet(
                        self.player.rect.centerx,
                        self.player.rect.top,
                        kind=self.weapon,
                        direction=-1,
                    ))

    def update(self):
        keys = pygame.key.get_pressed()
        self.player.move(keys, self.game_area)
        self._update_monsters()
        self._update_player_bullets()
        self._update_enemy_bullets()

    def _update_monsters(self):
        for monster in self.monsters:
            monster.move(self.width, self.height)
            if isinstance(monster, Shooter):
                shot = monster.try_shoot()
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
        for bullet in self.enemy_bullets:
            bullet.move()
        self.enemy_bullets = [b for b in self.enemy_bullets if not b.is_off_screen()]

    def draw(self):
        self.screen.fill((25, 25, 40))

        self.player.draw(self.screen)

        for monster in self.monsters:
            monster.draw(self.screen)
            self.health_bar.draw(self.screen, monster)

        for bullet in self.bullets + self.enemy_bullets:
            bullet.draw(self.screen)

        self._draw_hud()
        pygame.display.flip()

    def _draw_hud(self):
        score_text = self.font.render(f"Score : {self.score}", True, (255, 255, 255))
        weapon_text = self.font.render(f"Arme : {self.weapon}  (TAB)", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(weapon_text, (10, 40))

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()
