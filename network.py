import socket, _thread
from constants import *
decoder = 'utf-8'
PACKET_SIZE = 16000
PACKET_SUFFIX = b' _ '

def from_bytes_to_int(numbers):
    return int.from_bytes(numbers, BYTEORDER)

def handler_code_as_byte(handler_code_key):
    return HANDLER_CODES[handler_code_key].to_bytes(1, BYTEORDER)

def position_to_packet(position: tuple[int, int]):
    return position[0].to_bytes(POSITION_BYTE_LEN , BYTEORDER) + position[1].to_bytes(POSITION_BYTE_LEN , BYTEORDER)

def run_in_thread(func: ((...))):
    def run(*k, **kw):
        _thread.start_new_thread(func, k)
    return run

class Packet:
    def __init__(self, id, x, y, color, direction):
        self.id = id
        self.x = x
        self.y = y
        self.color = color
        self.direction = direction

class Client:
    def __init__(self, ip:str | tuple[int | float], port:int):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.addr = (ip, port)
        self.identifier = b"\x00"
        self.positions = {}
        self.responses = []

    def connect(self):
        try:
            self.client.sendto(self.identifier, self.addr)
            response = self.client.recv(PACKET_SIZE)
            self.identifier = response
            return response
        except Exception as e:
            print("error caught in 'connect': \n", e)
            return False

    @run_in_thread
    def query_positions(self, position):
        id_len = 1
        self.client.sendto(
            HANDLER_CODES["player_movement"].to_bytes(1,BYTEORDER) +
            self.identifier +
            position_to_packet(position),
            self.addr
        )
        response = self.client.recv(PACKET_SIZE)
        for packet in response.split(b" _ "):
            self.positions[packet[0]] = (
                (from_bytes_to_int(packet[id_len:POSITION_BYTE_LEN+id_len]),
                 from_bytes_to_int(packet[POSITION_BYTE_LEN+id_len:])
            ))


    @run_in_thread
    def send(self, data):
        try:
            self.client.sendto(data + PACKET_SUFFIX, self.addr)
            response = self.client.recv(PACKET_SIZE)
            self.responses = response.split(b" _ ")
            self.responses.pop() # removes trailing element after split
            return self.responses
        except socket.error as e:
            print(e)


index = 0

def IOTA(force=False) -> bytes:
    """
    ENUMERATOR
    """
    global index
    if force:
        index = 0
    index += 1
    return index.to_bytes(1,'big')

class Server:
    def __init__(self, ip:str | tuple[int | float], port:int) -> None:
        self.ip = ip
        self.port = port
        self.addr = (self.ip, self.port)
        self.all_players = {}
        self.addresses = []
        self.handlers = {}

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(self.addr)

    def new_connection(self, payload, address):
        self.sock.sendto(IOTA(), address)

    def player_movement(self, payload, address):
        self.all_players[payload[0]] = payload[1:]

        all_player_positions = [id.to_bytes(1, BYTEORDER) + self.all_players[id] for id in self.all_players.keys()]
        all_player_bytestring = b" _ ".join(all_player_positions)
        self.sock.sendto(all_player_bytestring, address)

    def projectile_generated(self, payload, address):
        response = payload
        self.sock.sendto(response, address)

    def player_animation_event(self, payload, address):
        response = payload
        self.sock.sendto(response, address)

    def hello_world(self, address):
        self.addresses.append(address)
        print(f"new connection from {address}!")

    def format_all_entities(self) -> bytes:
        players = self.all_players
        response = b''
        for id in players.keys():
            response += players[id]
        return response


    def run(self):
        print("server is listening...\n")

        handlers = {
            HANDLER_CODES["new_connection"] : Server.new_connection,
            HANDLER_CODES["player_movement"] : Server.player_movement,
            HANDLER_CODES["projectile_generated"] : Server.projectile_generated,
            HANDLER_CODES["player_animation_event"] : Server.player_animation_event,
        }
        while True:
            try:
                request, address = self.sock.recvfrom(PACKET_SIZE)
                signature = request[0]
                payload = request[1:]
                if address not in self.addresses:
                    self.hello_world(address)

                handlers[signature](self, payload, address)

            except Exception as e:
                self.sock.close()
                print("error handled succesfully")
                raise e

