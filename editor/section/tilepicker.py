from section.section import *

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
