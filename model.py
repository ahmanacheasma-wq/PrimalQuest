import pygame
from player import Player
from monster_types import create_random_monster
from abilities import Shooter
from bullet import Bullet


class GameModel:
    """Règles du jeu. Ne dessine rien et ne lit aucune touche (MVC)."""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.game_area = pygame.Rect(0, 0, width, height)
        self.weapons = ["bullet", "laser"]
        self.reset()

    def reset(self):
        """Remet la partie à zéro."""
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

    # ----- Actions -----

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

    # ----- Mise à jour à chaque image -----

    def update(self, keys):
        if self.game_over:
            return
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