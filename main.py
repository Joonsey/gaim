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
        self.network_client.send(
            NETWORK_ORDER["player"]
            + self.network_client.identifier
            + position_to_packet(self.player.position)
        )
        self.get_other_players()

        Particle.update_particles(self.particles, dt, self.scroll)

        if self.player._is_dashing:
            self.network_client.send(
                NETWORK_ORDER["spawn_particle"]
                + self.network_client.identifier
                + position_to_packet(self.player.position)
                + int(self.player.direction[0]).to_bytes(1, BYTEORDER, signed=True)
                + int(self.player.direction[1]).to_bytes(1, BYTEORDER, signed=True)
            )


    def get_other_players(self):
        for event in self.network_client.responses:
            event_type = event[0]


            if event_type == from_bytes_to_int(NETWORK_ORDER["player"]):
                id = event[1]
                if id == int.from_bytes(self.network_client.identifier, "little"):
                    continue

                x = from_bytes_to_int(event[2:POSITION_BYTE_LEN+2]) - self.scroll[0]
                y = from_bytes_to_int(event[2+POSITION_BYTE_LEN:]) - self.scroll[1]

                self.players[id] = Player(int(x), int(y), batch=self.player_batch)

            if event_type == from_bytes_to_int(NETWORK_ORDER['spawn_particle']):

                x = from_bytes_to_int(event[2:POSITION_BYTE_LEN+2])# - self.scroll[0]
                y = from_bytes_to_int(event[2+POSITION_BYTE_LEN:-2])# - self.scroll[1]
                _direction = event[-2], event[-1]
                direction = []
                for d in _direction:
                    if d == 1: 
                        v = -1
                    elif d == 255:
                        v = 1
                    else:
                        v = 0
                    direction.append(v)

                self.make_particle(x, y, direction = tuple(direction))

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

