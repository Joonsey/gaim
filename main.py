import pygame
from network.client import Client
import sys
from entities import *

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

        self.player = Player(0,0, size, size)
        self.client = Client(HOST, PORT)
        self.client.player_name = "Jae"
        self.client.start()
        self.scroll = [0,0]

        self.running = True

    def scroll_compensation(self, position):
        return position[0] - self.scroll[0], position[1] - self.scroll[1]

    def change_player_state(self, state: PlayerState):
        self.player.state = state
        self.client.broadcast_state(self.player.state)

    def run(self):
        while self.running:
            self.deltatime = self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            self.scroll[0] += (self.player.x - self.scroll[0] - (self.surf.get_width() / 2)) / 10
            self.scroll[1] += (self.player.y - self.scroll[1] - (self.surf.get_height() / 2)) / 10

            keys = pygame.key.get_pressed()
            self.player.handle_movement(keys, self.deltatime)

            self.client.broadcast_position(self.player.position)

            for other_player in self.client.players.copy():
                if other_player.id != self.client.id:
                    temp = pygame.surface.Surface((size, size))
                    temp.fill((0,234,23))
                    self.surf.blit(temp, self.scroll_compensation(other_player.position))
                    if other_player.name:
                        name = other_player.name.rstrip("\x00")
                        text_surf = font.render(name.capitalize(), False, (255,255,255, 255))
                        text_pos = (
                            other_player.position[0] - self.scroll[0],
                            other_player.position[1] - self.scroll[1]
                            -20)
                        self.surf.blit(text_surf, text_pos)

            self.player.surf.fill((242,24,24))
            self.surf.blit(self.player.surf, self.scroll_compensation(self.player.position))

            resized_surf = pygame.transform.scale(self.surf, self.display.get_size())
            self.display.blit(resized_surf, (0,0))
            pygame.display.flip()
            self.display.fill(0)
            self.surf.fill(0)

        self.client.stop()

if __name__ == "__main__":
    if "-l" in sys.argv:
        HOST = "localhost"
    game = Game(DISPLAY_DIMESION)
    game.run()


