import os
import pygame

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "images")


class Assets:
    """Charge les images depuis le dossier images. Renvoie None si l'image n'existe pas."""

    def __init__(self):
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