import pygame


class Controller:
    """Lit le clavier et la souris, et transmet les actions au jeu (MVC)."""

    def __init__(self, game, view):
        self.game = game
        self.view = view

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.stop()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.stop()
                elif event.key == pygame.K_TAB:
                    self.game.next_weapon()
                elif event.key == pygame.K_SPACE:
                    self.game.fire()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.view.button_rect.collidepoint(event.pos):
                    self.game.restart()

    def pressed_keys(self):
        return pygame.key.get_pressed()