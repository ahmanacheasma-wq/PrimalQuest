import pygame


class Player:
    """Singleton : une seule instance du joueur principal."""

    MAX_HEALTH = 8
    SIZE = 100

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return

        self.reset_state()
        self._initialized = True

    def reset_state(self):
        """Réinitialise le joueur sans créer une nouvelle instance."""
        self.rect = pygame.Rect(380, 420, self.SIZE, self.SIZE)
        self.speed = 7
        self.color = (50, 150, 255)
        self.max_health = self.MAX_HEALTH
        self.health = self.max_health
        self.invulnerability_timer = 0

    @property
    def is_alive(self):
        return self.health > 0

    def take_damage(self, amount):
        if self.invulnerability_timer > 0:
            return

        self.health = max(0, self.health - amount)
        self.invulnerability_timer = 75

    def heal(self, amount):
        self.health = min(
            self.max_health,
            self.health + max(0, amount)
        )

    def update(self):
        if self.invulnerability_timer > 0:
            self.invulnerability_timer -= 1

    def move(self, keys, game_area):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        self.rect.clamp_ip(game_area)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
