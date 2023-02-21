from particles import Dash_particle, Particle
from player import Player
from constants import *
from world import World
from network import Client
import pyglet
import sys
from sys import argv

def from_bytes_to_int(numbers):
    return int.from_bytes(numbers, BYTEORDER)

def position_to_packet(position: tuple[int, int]):
    return position[0].to_bytes(POSITION_BYTE_LEN , BYTEORDER) + position[1].to_bytes(POSITION_BYTE_LEN , BYTEORDER)

class Game(pyglet.window.Window):
    def __init__(self, *args):
        super(Game, self).__init__(*args)

        self.scroll:list[float]= [int(MAX_POSITION_BYTE_VAL/2), int(MAX_POSITION_BYTE_VAL/2)]
        self.network_client = Client(IP, PORT)
        self.network_client.connect()

        self.delta_player_count = 0

        self.world_batch = pyglet.graphics.Batch()
        self.player_batch = pyglet.graphics.Batch()
        self.particle_batch = pyglet.graphics.Batch()

        self.player = Player(int(MAX_POSITION_BYTE_VAL/2), int(MAX_POSITION_BYTE_VAL/2), batch=self.player_batch)
        self.world = World(self.world_batch)

        self.world.load_world_data("world.dat")
        self.world.make_world()

        self.players = {}
        self.particles = []

        self.keyboard = pyglet.window.key.KeyStateHandler()
        self.mouse = pyglet.window.mouse.MouseStateHandler()
        self.push_handlers(self.mouse)
        self.push_handlers(self.keyboard)

        self.client_events(self.keyboard, self.mouse)
        self.network_client.query_names()

        pyglet.clock.schedule_interval(self.draw, 1/FPS)
        pyglet.clock.schedule_interval(self.update, 1/FPS)

    def draw(self, dt):
        self.clear()
        self.world_batch.draw()
        self.player_batch.draw()
        self.particle_batch.draw()

    def update(self, dt):
        self.scroll[0] += (self.player.x - self.scroll[0]- (WIDTH/2)) / 14
        self.scroll[1] += (self.player.y - self.scroll[1]- (HEIGHT/2)) / 14

        self.world.update(self.scroll)

        self.player.handle_movement(self.keyboard, self.mouse, dt, self.scroll)
        self.network_client.query_positions(self.player.position)
        self.add_players_from_positions(self.network_client.positions)


        if len(self.network_client.positions) != self.delta_player_count:
            self.delta_player_count = len(self.network_client.positions)
            self.network_client.query_names()

        Particle.update_particles(self.particles, dt, self.scroll)

        if self.player._is_dashing:
            self.network_client.send(
                NETWORK_ORDER["spawn_particle"]
                + self.network_client.identifier
                + position_to_packet(self.player.position)
                + int(self.player.direction[0]).to_bytes(1, BYTEORDER, signed=True)
                + int(self.player.direction[1]).to_bytes(1, BYTEORDER, signed=True)
            )

    def add_players_from_positions(self, positions):
        for id, position in positions.items():
            if id == from_bytes_to_int(self.network_client.identifier):
                continue
            x = int(position[0] - self.scroll[0])
            y = int(position[1] - self.scroll[1])
            self.players[id] = Player(x, y, batch=self.player_batch)

        return self.players

    def make_particle(self, x, y, direction=(0,0), variation = None):
        self.particles.append(Dash_particle(x, y, 16, 16, 2, direction, self.particle_batch))

    def client_events(self, keyboard, mousehandler):
        from pyglet.window import key

        if keyboard[key.Q]:
            sys.exit()


if __name__ == "__main__":
    args = len(argv) > 1
    if args:
        if argv[1] == '-l':
            IP = "localhost"
    game = Game(WIDTH, HEIGHT)
    pyglet.app.run()

