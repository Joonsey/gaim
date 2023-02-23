import os
import pygame

class SpriteData:
    def __init__(self) -> None:
        self.sprites = []
        self.load_sprites()
        self.sprite_keys = {key+1:val for key, val in enumerate(self.sprites)}
        self.active = 0

    def load_sprites(self, path="assets/imgs"):
        try:
            file_names = os.listdir(path)
            for i, file_name in enumerate(file_names):
                file_path = os.path.join(path, file_name)
                tile = pygame.image.load(file_path)
                self.sprites.append(tile)
        except FileNotFoundError:
            print(f"asset path invalid: '{path}'")


TILE_SIZE = 32
MAX_ROWS = 150
MAX_COLUMNS = 150

WIDTH = 1080
HEIGHT = 720
