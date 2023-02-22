import pygame
import json
import os

TILE_SIZE = 32
MAX_ROWS = 150
MAX_COLUMNS = 150

WIDTH = 1080
HEIGHT = 720

#TODO not yet in use
class Tile:
    def __init__(self, surf) -> None:
        self.surf = surf
        self.active = False

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

    @staticmethod
    def parse_from_json(path: str = "config.json"):
        sections = []
        with open(path, "r") as f:
            config = json.load(f)

        for s in config["sections"]:
            rel_dim = s["relative_dimension"]
            eval_string = f'{s["type"]}((WIDTH*{rel_dim[0]},HEIGHT*{rel_dim[1]}), {s["color"]})'
            sec = eval(eval_string)
            sections.append(sec)
        return sections



class Tilepicker(Section):
    def __init__(self, dimensions, color) -> None:
        super().__init__(dimensions, color)

class Grid(Section):
    def __init__(self, dimensions, color) -> None:
        super().__init__(dimensions, color)
        self.background = None

    def set_background(self, surface):
        self.background = surface

    def draw(self):
        if self.background != None:
            self.surf.blit(self.background, (0,0))

        for col in range(MAX_COLUMNS):
            pygame.draw.line(self.surf, (222,222,222,120), (col*TILE_SIZE,0), (col*TILE_SIZE, HEIGHT))

        for row in range(MAX_ROWS):
            pygame.draw.line(self.surf, (222,222,222,120), (0, row*TILE_SIZE), (WIDTH, row*TILE_SIZE))

class Editor:
    def __init__(self, width, height, sections=[]) -> None:
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

if __name__ == "__main__":
    sections = Section.parse_from_json()
    editor = Editor(WIDTH, HEIGHT, sections)
    editor.run()
