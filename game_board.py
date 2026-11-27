import pygame
import os
import math
from array import array

from model import GameModel
from view import View
from health_bar import HealthBar


class GameBoard:
    """Assemble le Model, la View et le Controller."""

    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()

        self.width = 800
        self.height = 600

        self.screen = pygame.display.set_mode(
            (self.width, self.height)
        )

        pygame.display.set_caption("PrimalQuest")
        self.clock = pygame.time.Clock()

        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Musique de fond
        music_path = os.path.join(
            base_dir, "sounds", "background.mp3"
        )
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.3)

        # Son Game Over
        game_over_path = os.path.join(
            base_dir, "sounds", "game_over.mp3"
        )
        self.game_over_sound = pygame.mixer.Sound(game_over_path)
        self.game_over_sound.set_volume(0.7)

        self.game_over_played = False

        # Son du tir du joueur
        self.player_shot_sound = self.create_player_shot_sound()
        self.player_shot_sound.set_volume(0.35)

        self.model = GameModel(self.width, self.height)
        self.view = View(self.screen, self.width, self.height)
        self.health_bar = HealthBar()

        self.running = True
        self.started = False

    def create_player_shot_sound(self):
        """Crée un petit son électronique pour chaque tir."""

        sample_rate = 44100
        duration = 0.12
        samples = array("h")

        total_samples = int(sample_rate * duration)

        for i in range(total_samples):
            t = i / sample_rate
            progress = i / total_samples

            frequency = 850 - (400 * progress)
            envelope = (1 - progress) ** 2

            value = (
                math.sin(2 * math.pi * frequency * t)
                * envelope
                * 11000
            )

            samples.append(int(value))

        return pygame.mixer.Sound(buffer=samples.tobytes())

    # Actions du jeu

    def stop(self):
        self.running = False

    def next_weapon(self):
        self.model.next_weapon()

    def fire(self):
        self.model.fire()

    def restart(self):
        self.model.restart()
        self.game_over_played = False

        if self.started:
            pygame.mixer.music.play(-1)

    # Gestion des événements

    def process_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.stop()

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    self.stop()

                elif self.started and event.key == pygame.K_TAB:
                    self.next_weapon()

                elif self.started and event.key == pygame.K_SPACE:
                    self.fire()

            elif (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
            ):

                if not self.started:
                    if self.view.start_button_rect.collidepoint(event.pos):
                        self.started = True
                        self.model.reset()
                        pygame.mixer.music.play(-1)

                elif self.model.game_over:
                    if self.view.button_rect.collidepoint(event.pos):
                        self.restart()

    # Affichage

    def draw(self):
        m = self.model

        self.view.draw_world_background(m.background_path)
        self.view.draw_player(m.player)

        for monster in m.monsters:
            self.view.draw_monster(monster, self.health_bar)

        for bullet in m.bullets + m.enemy_bullets:
            self.view.draw_bullet(bullet)

        self.view.draw_info_panel(
            m.score,
            m.player.health,
            m.game_over
        )

        self.view.draw_level_info(
            m.level,
            m.level_time_left
        )

        if m.is_transitioning:
            self.view.draw_level_transition(m.level_message)

        if m.game_over:
            self.view.draw_game_over()

        pygame.display.flip()

    # Boucle principale

    def run(self):
        while self.running:

            self.process_events()

            if not self.running:
                break

            if not self.started:
                self.view.draw_start_screen()

            else:
                # Détecter les tirs du joueur
                old_bullets = len(self.model.bullets)

                self.model.update(
                    pygame.key.get_pressed()
                )

                new_bullets = len(self.model.bullets) > old_bullets

                if new_bullets:
                    self.player_shot_sound.play()

                # Son Game Over
                if (
                    self.model.game_over
                    and not self.game_over_played
                ):
                    pygame.mixer.music.stop()
                    self.game_over_sound.play()
                    self.game_over_played = True

                self.draw()

            self.clock.tick(60)

        pygame.quit()