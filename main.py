from network import Client
import pyglet
import sys

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

def position_to_packet(position: tuple[int, int]):
    return position[0].to_bytes(POSITION_BYTE_LEN , BYTEORDER) + position[1].to_bytes(POSITION_BYTE_LEN , BYTEORDER)

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
    
    def dash(self, speed: int, direction: tuple[float, float], t :float, scroll: tuple, total_t: int = 1) -> float:
        if total_t <= 0:
            return
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

        self.scroll = [int(MAX_POSITION_BYTE_VAL/2), int(MAX_POSITION_BYTE_VAL/2)]
        self.network_client = Client(IP, PORT)
        self.network_client.connect()

        self.player_batch = pyglet.graphics.Batch()

        self.player = Player(int(MAX_POSITION_BYTE_VAL/2), int(MAX_POSITION_BYTE_VAL/2), batch=self.player_batch)
        self.players = {}

        self.keyboard = pyglet.window.key.KeyStateHandler()
        self.mouse = pyglet.window.mouse.MouseStateHandler()
        self.push_handlers(self.mouse)
        self.push_handlers(self.keyboard)

        self.client_events(self.keyboard, self.mouse)

        pyglet.clock.schedule_interval(self.draw, 1/FPS)
        pyglet.clock.schedule_interval(self.update, 1/FPS)

    def draw(self, dt):
        self.clear()
        self.player_batch.draw() 

    def update(self, dt):

        self.scroll[0] += (self.player.x - self.scroll[0]- (WIDTH/2)) / 14
        self.scroll[1] += (self.player.y - self.scroll[1]- (HEIGHT/2)) / 14

        self.player.handle_movement(self.keyboard, self.mouse, dt, self.scroll)
        self.network_client.send(position_to_packet(self.player.position))
        self.get_other_players()

    def get_other_players(self):
        peepos = self.network_client.responses
        for peepo in peepos:
            id = peepo[0]
            if id == int.from_bytes(self.network_client.identifier, "little"):
                continue
            x = int.from_bytes(peepo[1:POSITION_BYTE_LEN+1], "little") - self.scroll[0]
            y = int.from_bytes(peepo[POSITION_BYTE_LEN+1:], "little") - self.scroll[1]

            #print("abs x: ", int.from_bytes(peepo[1:POSITION_BYTE_LEN+1], "little"))
            #print("x, y:", x, y)
            self.players[id] = Player(x, y, batch=self.player_batch)
        return self.players

    def client_events(self, keyboard, mousehandler):
        from pyglet.window import key

        if keyboard[key.Q]:
            sys.exit()

if __name__ == "__main__":
    game = Game(WIDTH, HEIGHT)
    pyglet.app.run()

