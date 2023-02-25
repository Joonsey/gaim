import pygame
from network.client import Client
DISPLAY_DIMESION = (1080, 720)
RENDER_DIMENSION = (540, 360)

size = 20
HOST = "84.212.18.137"
PORT = 5555
FPS = 60

pygame.init()

display = pygame.display.set_mode(DISPLAY_DIMESION)
surf = pygame.surface.Surface(RENDER_DIMENSION)

font = pygame.font.SysFont(pygame.font.get_default_font(), 36)

class Player:
    def __init__(self) -> None:
        self.surf = pygame.surface.Surface((size, size))
        self.x = 0
        self.y = 0


player = Player()
client = Client(HOST, PORT)
clock = pygame.time.Clock()

client.player_name = "tac"

client.start()
        
run = True
while run:
    clock.tick(FPS) 
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
        if other_player.id != client.id:
            temp = pygame.surface.Surface((size, size))
            temp.fill((0,234,23))
            surf.blit(temp, other_player.position)
            if other_player.name:
                name = other_player.name.rstrip("\x00")
                text_surf = font.render(name.capitalize(), False, (255,255,255, 255))
                text_pos = (other_player.position[0], other_player.position[1]-20)
                surf.blit(text_surf, text_pos)

    player.surf.fill((242,24,24))

    surf.blit(player.surf, (player.x, player.y))

    resized_surf = pygame.transform.scale(surf, display.get_size())
    display.blit(resized_surf, (0,0))
    pygame.display.flip()
    display.fill(0)
    surf.fill(0)


pygame.quit()
client.stop()