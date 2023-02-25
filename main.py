import pygame
from network.client import Client
DISPLAY_DIMESION = (1080, 720)
RENDER_DIMENSION = (540, 360)

size = 20
HOST = "84.212.18.137"
PORT = 5555

pygame.init()

display = pygame.display.set_mode(DISPLAY_DIMESION)
surf = pygame.surface.Surface(RENDER_DIMENSION)

class Player:
    def __init__(self) -> None:
        self.surf = pygame.surface.Surface((size, size))
        self.x = 0
        self.y = 0


player = Player()
client = Client(HOST, PORT)

name = input("insert name\n>>>")
client.player_name = name

client.start()
        
run = True
while run:
    surf = pygame.transform.smoothscale(surf, display.get_size())
    display.blit(surf, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        player.y -= 5
    if keys[pygame.K_s]:
        player.y += 5
    if keys[pygame.K_a]:
        player.x -= 5
    if keys[pygame.K_d]:
        player.x += 5

    client.broadcast_position((player.x, player.y))

    for other_player in client.players.copy():
        temp = pygame.surface.Surface((size, size))
        temp.fill((0,234,23))
        display.blit(temp, other_player.position)

    player.surf.fill((242,24,24))
    display.blit(player.surf, (player.x, player.y))
    pygame.display.flip()
    display.fill(0)


pygame.quit()
client.stop()
exit()