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

    def draw(self):
        self.surf.fill(self.color)

