import pygame
import os
import json
import pygame
from util.constants import *

class Section:
    def __init__(self, dimensions, color) -> None:
        self.surf = pygame.surface.Surface(dimensions)
        self.color = color
        self.surf.fill(self.color)
        self.sprites = []
        self.load_sprites()

    def load_sprites(self, path="assets/imgs"):
        try:
            file_names = os.listdir(path)
            for file_name in file_names:
                file_path = os.path.join(path, file_name)
                self.sprites.append(pygame.image.load(file_path))
        except FileNotFoundError:
            print(f"asset path invalid: '{path}'")

    def draw(self):
        for i, sprite in enumerate(self.sprites):
            self.surf.blit(sprite, (0,i*TILE_SIZE))


