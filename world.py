from constants import *
from tile import Tile
class World:
    def __init__(self, batch) -> None:
        self.batch = batch
        self.world_data = world_data
        self.tiles = []
        self.absolute_pos = (MAX_POSITION_BYTE_VAL/2, MAX_POSITION_BYTE_VAL/2)

    def load_world_data(self, path):
        world_data = []
        try:
            with open(path, "r") as f:
                for line in f.readlines():
                    world_data.append([int(x) for x in line.replace(" ","").split(",")])
        except Exception as e:
            print("problem with loading world data")

        if world_data:
            self.world_data = world_data


    def make_world(self):
        for y in range(len(self.world_data)):
            for x in range(len(self.world_data[y])):
                tile = self.world_data[y][x]
                if tile == 1:
                    self.tiles.append(Tile(
                        x*TILESIZE,
                        y*TILESIZE,
                        TILESIZE,
                        TILESIZE,
                        (255,255,255,255),
                        self.batch))

    def update(self, scroll):
        for tile in self.tiles:
            tile.rect.x =  int(self.absolute_pos[0] + tile.relative_pos[0] - scroll[0])
            tile.rect.y =  int(self.absolute_pos[1] + tile.relative_pos[1] - scroll[1])
