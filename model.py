
import pygame
import math

from game_observer import GameObserver
from observer import EventManager
from player import Player
from abilities import Shooter
from bullet import Bullet

from world_factory import (
    CaveWorldFactory,
    ForestWorldFactory,
    DesertWorldFactory
)


PLAY_AREA = pygame.Rect(90, 260, 630, 240)


class GameModel:
    """Règles du jeu : modèle MVC."""

    LEVEL_DURATION = 30_000
    TRANSITION_DURATION = 2500

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.game_area = PLAY_AREA

        self.events = EventManager()
        self.game_observer = GameObserver()
        self.events.subscribe(self.game_observer)

        self.reset()

    def reset(self):
        # Singleton : réutilise l'unique instance du joueur
        self.player = Player()
        self.player.reset_state()

        self.level = 1
        self.difficulty_tier = 1
        self.level_started_at = pygame.time.get_ticks()

        self.transition_until = None
        self.level_message = ""

        # Abstract Factory : monde initial
        self.world_factory = CaveWorldFactory()
        self.background_path = self.world_factory.create_background()

        self.weapons = self.world_factory.create_weapons()
        self.weapon_index = 0

        self.monsters = self._create_world_monsters(1)

        self.bullets = []
        self.enemy_bullets = []

        self.fire_cooldown = 0
        self.score = 0

        self._apply_difficulty()

        self.events.notify("game_reset")

    @property
    def weapon(self):
        return self.weapons[self.weapon_index]

    @property
    def game_over(self):
        return not self.player.is_alive

    @property
    def is_transitioning(self):
        return (
            self.transition_until is not None
            and pygame.time.get_ticks() < self.transition_until
        )

    @property
    def level_time_left(self):
        if self.is_transitioning:
            return self.LEVEL_DURATION // 1000

        elapsed = pygame.time.get_ticks() - self.level_started_at
        remaining = max(0, self.LEVEL_DURATION - elapsed)

        return (remaining + 999) // 1000

    def next_weapon(self):
        if not self.game_over and not self.is_transitioning:
            self.weapon_index = (
                self.weapon_index + 1
            ) % len(self.weapons)

    def fire(self):
        """Le joueur tire vers le monstre le plus proche."""

        if self.game_over or self.is_transitioning:
            return

        if self.fire_cooldown > 0 or not self.monsters:
            return

        monster = min(
            self.monsters,
            key=lambda m: (
                (m.rect.centerx - self.player.rect.centerx) ** 2
                + (m.rect.centery - self.player.rect.centery) ** 2
            )
        )

        dx = monster.rect.centerx - self.player.rect.centerx
        dy = monster.rect.centery - self.player.rect.centery

        if not math.isfinite(dx) or not math.isfinite(dy):
            print("Tir annulé : coordonnées invalides.")
            return

        length = math.hypot(dx, dy)

        if not math.isfinite(length) or length == 0:
            return

        ux = dx / length
        uy = dy / length

        half_width = self.player.rect.width / 2
        half_height = self.player.rect.height / 2

        distance_x = (
            half_width / abs(ux) if ux != 0 else float("inf")
        )

        distance_y = (
            half_height / abs(uy) if uy != 0 else float("inf")
        )

        distance = min(distance_x, distance_y) + 8

        start_x = self.player.rect.centerx + ux * distance
        start_y = self.player.rect.centery + uy * distance

        if not math.isfinite(start_x) or not math.isfinite(start_y):
            print("Tir annulé : position de balle invalide.")
            return

        self.bullets.append(
            Bullet(
                start_x,
                start_y,
                kind=self.weapon,
                direction=uy,
                dx=ux
            )
        )

        self.fire_cooldown = 12

    def restart(self):
        if self.game_over:
            self.reset()

    def update(self, keys):
        if self.game_over:
            return

        now = pygame.time.get_ticks()

        if self.transition_until is not None:
            if now < self.transition_until:
                return

            self.transition_until = None
            self.level_started_at = now

        if now - self.level_started_at >= self.LEVEL_DURATION:
            self._advance_progression()
            return

        self.player.update()

        if self.fire_cooldown > 0:
            self.fire_cooldown -= 1

        if keys[pygame.K_SPACE]:
            self.fire()

        self.player.move(keys, self.game_area)

        self._update_monsters()
        self._update_player_bullets()
        self._update_enemy_bullets()

    def _update_monsters(self):
        for monster in self.monsters:
            monster.move(self.game_area, self.player)

            if isinstance(monster, Shooter):
                shot = monster.try_shoot(self.player)

                if shot is not None:
                    self.enemy_bullets.append(shot)

    def _create_world_monsters(self, count=1):
        """Crée les monstres avec la factory du monde actuel."""

        monsters = self.world_factory.create_monsters(
            self.game_area,
            count
        )

        for monster in monsters:
            self._apply_monster_difficulty(monster)

        return monsters

    def _apply_monster_difficulty(self, monster):
        """Augmente la vitesse et la fréquence des tirs."""

        if not hasattr(monster, "_base_speed_x"):
            monster._base_speed_x = monster.speed_x
            monster._base_speed_y = monster.speed_y

        factor = min(
            2.8,
            1.0 + (self.difficulty_tier - 1) * 0.30
        )

        monster.speed_x = monster._base_speed_x * factor
        monster.speed_y = monster._base_speed_y * factor

        if isinstance(monster, Shooter):
            if not hasattr(monster, "base_shoot_interval"):
                monster.base_shoot_interval = monster.shoot_interval

            new_interval = monster.base_shoot_interval / factor

            monster.set_shoot_interval(
                max(20, int(new_interval))
            )

    def _apply_difficulty(self):
        for monster in self.monsters:
            self._apply_monster_difficulty(monster)

    def _advance_progression(self):
        """Passe au monde suivant et applique sa récompense."""

        if self.level < 3:
            self.level += 1

            if self.level == 2:
                self.world_factory = ForestWorldFactory()
                self.level_message = "NIVEAU 2 - FORET"

            elif self.level == 3:
                self.world_factory = DesertWorldFactory()
                self.level_message = "NIVEAU 3 - DESERT"

            self.background_path = self.world_factory.create_background()
            self.weapons = self.world_factory.create_weapons()
            self.weapon_index = 0

            # Récompense du nouveau monde
            self._apply_world_reward()

        else:
            self.difficulty_tier += 1
            self.level_message = (
                f"DESERT - DIFFICULTE {self.difficulty_tier}"
            )

        # Un monstre au niveau 1, deux au niveau 2, trois au niveau 3
        monster_count = self.level
        self.monsters = self._create_world_monsters(monster_count)

        self.bullets.clear()
        self.enemy_bullets.clear()

        self.transition_until = (
            pygame.time.get_ticks() + self.TRANSITION_DURATION
        )

        print(self.level_message)

    def _apply_world_reward(self):
        """Applique la récompense fournie par la factory."""

        reward = self.world_factory.create_reward()

        health_bonus = reward.get("health_bonus", 0)
        score_bonus = reward.get("score_bonus", 0)

        self.player.heal(health_bonus)

        self.score += score_bonus
        self.events.notify("score_changed", self.score)

        print(
            f"Récompense obtenue : {reward['name']} "
            f"| Vie : +{health_bonus} "
            f"| Score : +{score_bonus}"
        )

    def _replace_monster(self, dead):
        if dead in self.monsters:
            self.monsters.remove(dead)

        self.score += 1
        self.events.notify("score_changed", self.score)

        if not self.monsters:
            self.monsters = self._create_world_monsters(self.level)

    def _update_player_bullets(self):
        for bullet in list(self.bullets):
            bullet.move()
            target = self._find_target(bullet)

            if target is not None:
                self.bullets.remove(bullet)
                target.take_damage(bullet)

                if not target.is_alive:
                    self._replace_monster(target)

            elif bullet.is_off_screen():
                self.bullets.remove(bullet)

    def _find_target(self, bullet):
        for monster in self.monsters:
            if monster.is_alive and bullet.rect.colliderect(monster.rect):
                return monster

        return None

    def _update_enemy_bullets(self):
        for bullet in list(self.enemy_bullets):
            bullet.move()

            if bullet.rect.colliderect(self.player.rect):
                self.player.take_damage(bullet.damage)

                self.events.notify(
                    "player_damaged",
                    self.player.health
                )

                self.enemy_bullets.remove(bullet)

            elif bullet.is_off_screen():
                self.enemy_bullets.remove(bullet)
