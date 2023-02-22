from section.section import *

class Grid(Section):
    def __init__(self, dimensions, color) -> None:
        super().__init__(dimensions, color)
        self.background = None
        self.show_grid = True

    def toggle_grid(self):
        self.show_grid = not self.show_grid

    def set_background(self, surface):
        self.background = surface

    def draw(self):
        super().draw()
        if self.background != None:
            self.surf.blit(self.background, (0,0))

        if self.show_grid:
            for col in range(MAX_COLUMNS):
                pygame.draw.line(self.surf, (222,222,222,120), (col*TILE_SIZE,0), (col*TILE_SIZE, HEIGHT))

            for row in range(MAX_ROWS):
                pygame.draw.line(self.surf, (222,222,222,120), (0, row*TILE_SIZE), (WIDTH, row*TILE_SIZE))
