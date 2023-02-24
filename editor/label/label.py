import pygame
import os

class Label:
    def __init__(self, size, font_path=""):
        if not font_path:
            self.font = pygame.font.SysFont(pygame.font.get_default_font(), size)
        else:
            self.font = pygame.font.Font(font_path, size)

    def make_text_surf(self, text, color=(255,255,255,255)):
        return self.font.render(text, False, color)


