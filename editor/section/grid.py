from section.section import *
from label.label import Label

class Grid(Section):
    def __init__(self, dimensions, color, **kwargs) -> None:
        super().__init__(dimensions, color, **kwargs)
        self.background = None
        self.show_grid = True
        self.world_data = [[-1 for _ in range(MAX_ROWS)] for __ in range(MAX_COLUMNS)]
        self.active_tile = None
        self.has_mouse_event = True
        self.ghost_position = (-1, -1)
        self.show_ghost = False
        self.is_scrolling = True
        self.scroll = [0,(MAX_COLUMNS * TILE_SIZE) - HEIGHT]
        self.prev_mouse_position = [0,0]
        self.label = Label(24, "assets/fonts/Hurmit Medium Nerd Font Complete.otf")
        self.grid_cursor_position = (0,0)

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

    def draw_ghost_tile(self, tile, position, opacity=128):
        ghost = tile.copy()
        ghost.set_alpha(opacity)
        self.surf.blit(ghost, position)

    def set_active_tile(self, tile):
        assert type(tile) == int
        self.sprite_data.active = tile

    def toggle_grid(self):
        self.show_grid = not self.show_grid

    def set_background(self, surface):
        self.background = surface

    def handle_mouse_event(self, mouse, cursor):
        rect = self.surf.get_bounding_rect()
        if self.has_offset:
            rect.left += self.offset[0]
            rect.top += self.offset[1]
        if rect.collidepoint(cursor):
            x = (cursor[0] + self.scroll[0]) // TILE_SIZE
            y = (cursor[1] + self.scroll[1]) // TILE_SIZE


            if self.has_offset:
                x = int((cursor[0] + self.scroll[0] - self.offset[0]) // TILE_SIZE)
                y = int((cursor[1] + self.scroll[1] - self.offset[1]) // TILE_SIZE)

            self.grid_cursor_position = (x,y)

            if self.sprite_data.active and self.world_data[y][x] == -1:
                self.show_ghost = True
                self.ghost_position = (x,y)
            else:
                self.show_ghost = False

            if self.is_scrolling and mouse[0]:
                self.scroll[0] += self.prev_mouse_position[0] - cursor[0]
                self.scroll[1] += self.prev_mouse_position[1] - cursor[1]
                if self.scroll[0] < 0:
                    self.scroll[0] = 0
                if self.scroll[1] < 0:
                    self.scroll[1] = 0
                if self.scroll[0] > MAX_ROWS * TILE_SIZE:
                    self.scroll[0] = MAX_ROWS * TILE_SIZE
                if self.scroll[1] > (MAX_COLUMNS * TILE_SIZE) - HEIGHT:
                    self.scroll[1] = (MAX_COLUMNS * TILE_SIZE) - HEIGHT

            self.prev_mouse_position = cursor

            if mouse[0]:
                try:
                    if self.sprite_data.active > -1:
                        self.world_data[y][x] = self.sprite_data.active
                        self.is_scrolling = False
                    else:
                        self.is_scrolling = True
                except:
                    #out of bounds
                    pass

            if mouse[2]:
                    self.world_data[y][x] = -1

    def draw(self):
        super().draw()
        if self.background != None:
            self.surf.blit(self.background, (0,0))

        text_content = f"{self.grid_cursor_position[0]},{self.grid_cursor_position[1]}"
        label = self.label.make_text_surf(text_content)
        self.surf.blit(label, (0,0))

        for y in range(len(self.world_data)):
            for x, tile in enumerate(self.world_data[y]):
                x_position = x*TILE_SIZE - self.scroll[0]
                y_position = y*TILE_SIZE - self.scroll[1]
                position = (x_position, y_position)
                if tile > 0:
                    self.surf.blit(self.sprite_data.sprites[tile], position)

                if (x,y) == self.ghost_position and self.show_ghost:
                    self.draw_ghost_tile(self.sprite_data.sprites[self.sprite_data.active], position)

        if self.show_grid:
            for col in range(MAX_COLUMNS):
                x_position = col*TILE_SIZE - self.scroll[0]
                pygame.draw.line(self.surf, (222,222,222,120), (x_position, 0), (x_position, HEIGHT))

            for row in range(MAX_ROWS):
                y_position = row*TILE_SIZE - self.scroll[1]
                pygame.draw.line(self.surf, (222,222,222,120), (0, y_position), (WIDTH, y_position))
