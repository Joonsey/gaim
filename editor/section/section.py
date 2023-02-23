import pygame
import json
from util.constants import *

class Section:
    def __init__(self, dimensions, color,  **kwargs) -> None:
        try:
            self.sprite_data = kwargs["sprite_data"]
        except:
            self.sprite_data = SpriteData()
        self.has_offset = False

        if "offset" in kwargs.keys():
            self.offset = kwargs["offset"]
            self.has_offset = True
        self.surf = pygame.surface.Surface(dimensions)
        self.color = color
        self.surf.fill(self.color)
        self.has_mouse_event = False
    
    def draw(self):
        self.surf.fill(self.color)

    def handle_mouse_event(self, mouse, cursor):
        raise NotImplementedError

