import pygame
from network.client import Client
import sys
from entities import *

DISPLAY_DIMESION = (1080, 720)
RENDER_DIMENSION = (540, 360)

size = 20
HOST = "84.212.18.137"
PORT = 5555
FPS = 60

pygame.init()

font = pygame.font.SysFont(pygame.font.get_default_font(), 12)

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

        self.running = True

    def run(self):
        while self.running:
            self.deltatime = self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            keys = pygame.key.get_pressed()
            self.player.handle_movement(keys, self.deltatime)

            self.client.broadcast_position(self.player.position)

            for other_player in self.client.players.copy():
                print(other_player)
                if other_player.id != self.client.id:
                    temp = pygame.surface.Surface((size, size))
                    temp.fill((0,234,23))
                    self.surf.blit(temp, other_player.position)
                    if other_player.name:
                        name = other_player.name.rstrip("\x00")
                        text_surf = font.render(name.capitalize(), False, (255,255,255, 255))
                        text_pos = (other_player.position[0], other_player.position[1]-20)
                        self.surf.blit(text_surf, text_pos)

            self.player.surf.fill((242,24,24))
            self.surf.blit(self.player.surf, (self.player.x, self.player.y))

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


