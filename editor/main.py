import pygame

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
    def __init__(self, width, height) -> None:
        self.surface = pygame.display.set_mode((width, height))
        self.grid = Grid((width, height), (5,5,5))
        self.tilepicker = Tilepicker((width/5, height), (22,21,23))
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            self.grid.draw()
            self.tilepicker.draw()
            self.surface.blit(self.grid.surf, (0,0))
            self.surface.blit(self.tilepicker.surf, (0,0))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()

if __name__ == "__main__":
    editor = Editor(WIDTH, HEIGHT)
    editor.run()
