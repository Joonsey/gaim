from entities import Player

class World:
    def __init__(self, tilesize, game_surf) -> None:
        self.player = Player(0,0, tilesize, tilesize)
        self.surf = game_surf
        self.tilesize = tilesize
        self.world_data = [[]]
