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

HANDLER_CODES = {
    "new_connection" : 0,
    "player_movement" : 1,
    "projectile_generated" : 2,
    "player_animation_event" : 3,
}

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
