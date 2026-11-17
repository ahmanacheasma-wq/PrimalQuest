import pygame
from player import Player
from monster_types import create_random_monster
from abilities import Shooter
from health_bar import HealthBar
from bullet import Bullet
from view import View
from controller import Controller


class GameBoard:
    def __init__(self):
        pygame.init()

        self.width = 800
        self.height = 600

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("PrimalQuest")

        self.clock = pygame.time.Clock()
        self.game_area = self.screen.get_rect()

        self.view = View(self.screen, self.width, self.height)
        self.controller = Controller(self, self.view)
        self.health_bar = HealthBar()
        self.weapons = ["bullet", "laser"]

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

    # ----- Actions demandées par le Controller -----

    def stop(self):
        self.running = False

    def next_weapon(self):
        if not self.game_over:
            self.weapon_index = (self.weapon_index + 1) % len(self.weapons)

    def fire(self):
        if not self.game_over:
            self.bullets.append(Bullet(
                self.player.rect.centerx,
                self.player.rect.top,
                kind=self.weapon,
                direction=-1,
            ))

    def restart(self):
        if self.game_over:
            self.reset()

    # ----- Logique du jeu (Model) -----

    def update(self, keys):
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

    # ----- Affichage (délégué à la View) -----

    def draw(self):
        self.view.draw_background()

        self.view.draw_player(self.player)

        for monster in self.monsters:
            self.view.draw_monster(monster, self.health_bar)

        for bullet in self.bullets + self.enemy_bullets:
            self.view.draw_bullet(bullet)

        self.view.draw_info_panel(self.score, self.player.health)

        if self.game_over:
            self.view.draw_game_over()

        pygame.display.flip()

    # ----- Boucle principale -----

    def run(self):
        while self.running:
            self.controller.process_events()
            if not self.game_over:
                self.update(self.controller.pressed_keys())
            self.draw()
            self.clock.tick(60)

        pygame.quit()