import pygame
from model import GameModel
from view import View
from controller import Controller
from health_bar import HealthBar


class GameBoard:
    """Assemble le Model, la View et le Controller, et lance la boucle de jeu."""

    def __init__(self):
        pygame.init()

        self.width = 800
        self.height = 600

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("PrimalQuest")
        self.clock = pygame.time.Clock()

        self.model = GameModel(self.width, self.height)
        self.view = View(self.screen, self.width, self.height)
        self.controller = Controller(self, self.view)
        self.health_bar = HealthBar()

        self.running = True

    # ----- Actions demandées par le Controller -----

    def stop(self):
        self.running = False

    def next_weapon(self):
        self.model.next_weapon()

    def fire(self):
        self.model.fire()

    def restart(self):
        self.model.restart()

    # ----- Affichage (délégué à la View) -----

    def draw(self):
        m = self.model

        self.view.draw_background()
        self.view.draw_player(m.player)

        for monster in m.monsters:
            self.view.draw_monster(monster, self.health_bar)

        for bullet in m.bullets + m.enemy_bullets:
            self.view.draw_bullet(bullet)

        self.view.draw_info_panel(m.score, m.player.health)

        if m.game_over:
            self.view.draw_game_over()

        pygame.display.flip()

    # ----- Boucle principale -----

    def run(self):
        while self.running:
            self.controller.process_events()
            self.model.update(self.controller.pressed_keys())
            self.draw()
            self.clock.tick(60)

        pygame.quit()