import os
import pygame

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "images")


class Assets:
    """Singleton : une seule instance pour gérer les ressources graphiques."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Assets, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_cache"):
            self._cache = {}

    def image(self, relative_path, size=None):
        key = (relative_path, size)

        if key not in self._cache:
            path = os.path.join(IMAGES_DIR, relative_path)

            if os.path.exists(path):
                image = pygame.image.load(path).convert_alpha()

                if size is not None:
                    image = pygame.transform.scale(image, size)
            else:
                image = None

            self._cache[key] = image

        return self._cache[key]