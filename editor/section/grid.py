from section.section import *

class Grid(Section):
    def __init__(self, dimensions, color, **kwargs) -> None:
        super().__init__(dimensions, color, **kwargs)
        self.background = None
        self.show_grid = True
        self.world_data = [[0 for x in range(MAX_ROWS)] for y in range(MAX_COLUMNS)]
        self.active_tile = None
        self.has_mouse_event = True

    def save_world(self, path: str= "level.json"):
        try:
            with open(path, "w+") as fp:
                json.dump(self.world_data, fp)
        except:
            print("unable to save world data")

    def load_world_data(self, path: str= "level.json"):
        try:
            with open(path, "r") as f:
                self.world_data = json.load(f)
        except:
            print("unable to load world data")

    def set_active_tile(self, tile):
        assert type(tile) == int
        self.sprite_data.active = tile

    def toggle_grid(self):
        self.show_grid = not self.show_grid

    def set_background(self, surface):
        self.background = surface

    def handle_mouse_event(self, mouse, cursor):
        if mouse[0] and self.surf.get_bounding_rect().collidepoint(cursor):
            if self.sprite_data.active:
                x = cursor[0] // TILE_SIZE
                y = cursor[1] // TILE_SIZE
                self.world_data[y][x] = self.sprite_data.active

        if mouse[2] and self.surf.get_bounding_rect().collidepoint(cursor):
                x = cursor[0] // TILE_SIZE
                y = cursor[1] // TILE_SIZE
                self.world_data[y][x] = 0


    def draw(self):
        super().draw()
        if self.background != None:
            self.surf.blit(self.background, (0,0))

        for y in range(len(self.world_data)):
            for x, tile in enumerate(self.world_data[y]):
                if tile > 0:
                    self.surf.blit(self.sprite_data.sprites[tile-1], (x*TILE_SIZE, y*TILE_SIZE))

        if self.show_grid:
            for col in range(MAX_COLUMNS):
                pygame.draw.line(self.surf, (222,222,222,120), (col*TILE_SIZE,0), (col*TILE_SIZE, HEIGHT))

            for row in range(MAX_ROWS):
                pygame.draw.line(self.surf, (222,222,222,120), (0, row*TILE_SIZE), (WIDTH, row*TILE_SIZE))
