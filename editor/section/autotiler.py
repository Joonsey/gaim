from section.section import *

class Autotiler(Section):
    def __init__(self, dimensions, color, **kwargs) -> None:
        super().__init__(dimensions, color, **kwargs)
        self.active = True
        self.has_mouse_event = True
        self.grid_data = [[-1 for _ in range(5)] for __ in range(5)]
        self.margin = 2
        self.tiles = {}

    def save_world(self, path: str= "auto_tiles.json"):
        try:
            with open(path, "w+") as fp:
                json.dump(self.grid_data, fp)
        except:
            print("unable to save world data")

    def load_world_data(self, path: str= "auto_tiles.json"):
        try:
            with open(path, "r") as f:
                self.grid_data = json.load(f)
        except:
            print("unable to load world data")
    
    def draw(self):
        super().draw()
        offset_to_center_x = (5 * TILE_SIZE - self.surf.get_width()) / 2
        offset_to_center_y = (5 * TILE_SIZE - self.surf.get_height()) / 2
        for y, column in enumerate(self.grid_data):
            for x, key in enumerate(column):
                if key >= 0:
                    tile = self.sprite_data.sprite_keys[key].copy()
                else:
                    tile = pygame.surface.Surface((TILE_SIZE, TILE_SIZE))
                #tile.set_colorkey((0,0,0,0))
                self.tiles[x,y] = self.surf.blit(tile, (x*TILE_SIZE - offset_to_center_x, y*TILE_SIZE - offset_to_center_y))

    def handle_mouse_event(self, mouse, cursor):
        for key, tile in self.tiles.items():
            if self.has_offset:
                tile.left += self.offset[0]
                tile.top += self.offset[1]
            if tile.collidepoint(cursor) and mouse[0]:
                x = key[0]
                y = key[1]
                if self.grid_data[y][x] != self.sprite_data.active:
                    self.grid_data[y][x] = self.sprite_data.active

            if tile.collidepoint(cursor) and mouse[2]:
                x = key[0]
                y = key[1]
                self.grid_data[y][x] = -1


        
