from network import Client
import pyglet
import sys

IP = "LOCALHOST"
PORT = 5555
FPS = 120
TPS = 20

BYTEORDER = "little"
POSITION_BYTE_LEN = 4

def position_to_packet(position: tuple[int, int]):
    return position[0].to_bytes(POSITION_BYTE_LEN , BYTEORDER) + position[1].to_bytes(POSITION_BYTE_LEN , BYTEORDER)

class Player():
    def __init__(self, x: int, y: int, batch=None) -> None:
        self.x = x
        self.y = y
        self.batch = batch
        self.position = self.x, self.y
        self._rect = pyglet.shapes.Rectangle(self.x, self.y, 25, 25, color=(255, 255, 0), batch=self.batch)

    def _update_pos(self, x, y):
        self.x = x
        self.y = y
        self.position = self.x, self.y
        self._rect.x = x
        self._rect.y = y

    def update(self, keyboard, dt):
        from pyglet.window import key

        if keyboard[key.W]:
            self.y += 10

        if keyboard[key.S]:
            self.y -= 10

        if keyboard[key.A]:
            self.x -= 10

        if keyboard[key.D]:
            self.x += 10

        #if keyboard[key.Q]:
            #sys.exit()

        self._update_pos(self.x, self.y)

class Game(pyglet.window.Window):
    def __init__(self):
        super(Game, self).__init__()

        self.network_client = Client(IP, PORT)
        self.network_client.connect()

        self.player_batch = pyglet.graphics.Batch()

        self.player = Player(100, 100, batch=self.player_batch)
        self.players = {}

        self.keyboard = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keyboard)

        self.client_events(self.keyboard)

        pyglet.clock.schedule_interval(self.draw, 1/FPS)
        pyglet.clock.schedule_interval(self.update, 1/TPS)

    def draw(self, dt):
        self.clear()
        self.player_batch.draw() 

    def update(self, dt):
        self.player.update(self.keyboard, dt)
        self.network_client.send(position_to_packet(self.player.position))
        self.get_other_players()

    def get_other_players(self):
        peepos = self.network_client.responses
        for peepo in peepos:
            id = peepo[0]
            if id == int.from_bytes(self.network_client.identifier, "little"):
                continue
            x = int.from_bytes(peepo[1:3], "little")
            y = int.from_bytes(peepo[5:-1], "little")
            self.players[id] = Player(x, y, batch=self.player_batch)
        return self.players

    def client_events(self, keyboard):
        from pyglet.window import key

        if keyboard[key.Q]:
            sys.exit()

if __name__ == "__main__":
    game = Game()
    pyglet.app.run()

