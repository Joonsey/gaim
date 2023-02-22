import pygame
import json
import os
from util.constants import *
from section import *

#TODO not yet in use
class Tile:
    def __init__(self, surf) -> None:
        self.surf = surf
        self.active = False

class Editor:
    def __init__(self, width, height, sections = []) -> None:
        self.surface = pygame.display.set_mode((width, height))
        self.sections = sections
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            for section in self.sections:
                section.draw()
                self.surface.blit(section.surf, (0,0))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_g:
                        for sec in self.sections:
                            if type(sec) == Grid:
                                sec.toggle_grid()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_q]:
                self.running = False
                pygame.quit()


    @staticmethod
    def parse_from_json(path: str = "config.json") -> list[Section]:
        sections = []
        with open(path, "r") as f:
            config = json.load(f)

        for s in config["sections"]:
            rel_dim = s["relative_dimension"]
            eval_string = f'{s["type"]}((WIDTH*{rel_dim[0]},HEIGHT*{rel_dim[1]}), {s["color"]})'
            sec = eval(eval_string)
            sections.append(sec)
        return sections

if __name__ == "__main__":
    sections = Editor.parse_from_json()
    editor = Editor(WIDTH, HEIGHT, sections)
    editor.run()
