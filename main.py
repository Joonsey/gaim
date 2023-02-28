import pygame
import network.client
import sys
from entities import *
from world.world import World

DISPLAY_DIMESION = (1080, 720)
RENDER_DIMENSION = (540, 360)

size = 16
HOST = "84.212.18.137"
PORT = 5555
FPS = 60

pygame.init()

font = pygame.font.SysFont(pygame.font.get_default_font(), 16)

class Game:
    def __init__(self, DISPLAY_DIMESION) -> None:
        self.display = pygame.display.set_mode(DISPLAY_DIMESION)
        self.surf = pygame.surface.Surface((540, 360))
        self.clock = pygame.time.Clock()
        self.deltatime = 0

        self.world = World(size, self.surf)
        self.player = self.world.player
        self.client = network.client.Client(HOST, PORT)
        self.client.player_name = "Jae"
        self.scroll = [0,0]

        self.running = True

    def render_entities(self, entities) -> None:
        for entity in entities.copy():
            if isinstance(entity, network.client.Player):
                # doesn't render if it's the current player
                # ideally it should NOT include the player in the packet form the server
                if entity.id != self.client.id:
                    entity_surf = pygame.surface.Surface((size, size))
                    entity_surf.fill((0,234,23))
                    self.surf.blit(entity_surf, self.scroll_compensation(entity.position))

            if isinstance(entity, network.client.Enemy):
                entity_surf = pygame.surface.Surface((size, size))
                entity_surf.fill((234,23,2))
                self.surf.blit(entity_surf, self.scroll_compensation(entity.position))

    def scroll_compensation(self, position):
        return position[0] - self.scroll[0], position[1] - self.scroll[1]

    def change_player_state(self, state: PlayerState):
        self.player.state = state
        self.client.broadcast_state(self.player.state)

    def run(self):
        self.client.start()
        while self.running:
            self.deltatime = self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.scroll[0] += (self.player.x - self.scroll[0] - (self.surf.get_width() / 2)) / 10
            self.scroll[1] += (self.player.y - self.scroll[1] - (self.surf.get_height() / 2)) / 10

            keys = pygame.key.get_pressed()
            prev_state = self.player.state

            self.player.handle_movement(keys, self.deltatime)
            if prev_state != self.player.state:
                self.client.broadcast_state(self.player.state)

            self.client.broadcast_position(self.player.position)

            self.render_entities(self.client.players.copy())
            self.render_entities(self.client.enemies.copy())

            self.player.animate()
            self.surf.blit(self.player.surf, self.scroll_compensation(self.player.position))

            # rendering the surf on display
            resized_surf = pygame.transform.scale(self.surf, self.display.get_size())
            self.display.blit(resized_surf, (0,0))
            pygame.display.flip()
            self.display.fill(0)
            self.surf.fill(0)

        self.client.stop()
        pygame.quit()


if __name__ == "__main__":
    if "-l" in sys.argv:
        HOST = "localhost"
    game = Game(DISPLAY_DIMESION)
    game.run()


