import pyglet

class Tile:
    def __init__(self, x, y, width, height, color, batch) -> None:
        self.rect = pyglet.shapes.Rectangle(x, y, width, height, color, batch)
        self.relative_pos = (x, y)
