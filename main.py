from network import Client
import pyglet
import sys
from sys import argv

from random import randint

IP = "84.212.18.137"
PORT = 5555
FPS = 120
TPS = 20
WIDTH = 1080
HEIGHT = 720

SPEED = 220

BYTEORDER = "little"
POSITION_BYTE_LEN = 4
MAX_POSITION_BYTE_VAL = POSITION_BYTE_LEN **16

NETWORK_ORDER = {
    "player" : b"\x01",
    "spawn_particle" : b"\xff",
    "hostile" : b"\x02",
}
world_data = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
]

TILESIZE = 32

class Tile:
    def __init__(self, x, y, width, height, color, batch) -> None:
        self.rect = pyglet.shapes.Rectangle(x, y, width, height, color, batch)
        self.relative_pos = (x, y)

class World:
    def __init__(self, batch) -> None:
        self.batch = batch
        self.world_data = world_data
        self.tiles = []
        self.absolute_pos = (MAX_POSITION_BYTE_VAL/2, MAX_POSITION_BYTE_VAL/2)

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

def update_particles(particles: list, dt, scroll):
    for particle in particles:
        particle.update(dt, scroll)
        if particle.lifetime == None or particle.lifetime < 0:
            particles.remove(particle)


def from_bytes_to_int(numbers):
    return int.from_bytes(numbers, BYTEORDER)

def position_to_packet(position: tuple[int, int]):
    return position[0].to_bytes(POSITION_BYTE_LEN , BYTEORDER) + position[1].to_bytes(POSITION_BYTE_LEN , BYTEORDER)

class Particle:
    def __init__(self, x: int, y: int, lifetime:float | None, batch=None) -> None:
        self.x = x
        self.y = y
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.absolute_position = self.x, self.y
        self.batch = batch

    def update(self, dt):
        if self.lifetime != None:
            self.lifetime -= dt
            if self.lifetime < 0:
                self.lifetime == None

class Dash_particle(Particle):
    def __init__(self,
                 x: int,
                 y: int,
                 w: int,
                 h: int,
                 lifetime: float,
                 direction: tuple,
                 batch=None) -> None:
        super().__init__(x, y, lifetime, batch)
        self.rect = pyglet.shapes.Rectangle(x, y, w, h, batch=batch)
        self.direction = direction
        self.speed = 2
        self.base_error = 2
        self.erro_modifier = 5

    def calc_error(self):
        if self.lifetime != None and self.max_lifetime != None:
            return randint(-self.base_error, self.base_error) / (self.max_lifetime +1 - self.lifetime)
        else:
            return 0

    def update(self, dt, scroll):
        super().update(dt)
        if self.lifetime != None and self.max_lifetime != None:
            error = self.calc_error()
            self.x += self.direction[0] * self.speed + error
            self.y += self.direction[1] * self.speed + error
            self.rect.x = int(self.x - scroll[0])
            self.rect.y = int(self.y - scroll[1])

            self.rect.width = self.rect.width * (self.lifetime / self.max_lifetime)
            self.rect.height = self.rect.height * (self.lifetime / self.max_lifetime)
            #print((self.x, self.y), self.direction)

class Player():
    def __init__(self, x: int, y: int, batch=None) -> None:
        self.x = x
        self.y = y
        self.batch = batch
        self.position = self.x, self.y
        self._rect = pyglet.shapes.Rectangle(self.x, self.y, 25, 25, color=(255, 255, 0), batch=self.batch)
        self.direction = [0,0]
        self.dash_cooldown = 2
        self.dash_duration = .2
        self._max_dash_duration = .2
        self._is_dashing = False

    def _update_pos(self, x, y, scroll):
        self.x = x
        self.y = y
        self.position = int(self.x), int(self.y)
        self._rect.x = x - scroll[0]
        self._rect.y = y - scroll[1]

    def dash(self, speed: int, direction: list|tuple[float | int, float | int], t :float, scroll: tuple, total_t: float|int = 1) -> float:
        if total_t <= 0:
            return self._max_dash_duration
        x = self.x + speed * direction[0] * t
        y = self.y + speed * direction[1] * t

        self._update_pos(x, y, scroll)
        return total_t-t if total_t-t > 0 else self._max_dash_duration

    def handle_movement(self, keyboard, mousehandler, dt, scroll):
        from pyglet.window import key
        from pyglet.window import mouse

        if self.dash_cooldown > 0: self.dash_cooldown -= dt

        if (mousehandler[mouse.LEFT] and self.dash_cooldown <= 0) or self.dash_duration != self._max_dash_duration:
            self.dash_cooldown = 2
            self.dash_duration = self.dash(SPEED*2, self.direction, dt, scroll, self.dash_duration)
            self._is_dashing = True
        else:
            self._is_dashing = False

        if keyboard[key.W]:
            self.direction[1] = 1

        elif keyboard[key.S]:
            self.direction[1] = -1

        else:
            self.direction[1] = 0

        if keyboard[key.A]:
            self.direction[0] = -1

        elif keyboard[key.D]:
            self.direction[0] = 1

        else:
            self.direction[0] = 0

        if keyboard[key.Q]:
            sys.exit()


        if self.direction[0] and self.direction[1]:
            self.direction = [i/2 for i in self.direction] #TODO ask leon about this lmao
            x = self.x + self.direction[0] * SPEED * dt
            y = self.y + self.direction[1] * SPEED * dt

        else:
            x = self.x + self.direction[0] * SPEED * dt
            y = self.y + self.direction[1] * SPEED * dt


        self._update_pos(x, y, scroll)


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

        update_particles(self.particles, dt, self.scroll)

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

