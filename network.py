import socket, _thread
decoder = 'utf-8'
PACKET_SIZE = 16000

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
        self.responses = {}

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
    def listen(self):
        try:
            response = self.client.recv(PACKET_SIZE).decode(decoder)
            return response
        except:
            pass


    @run_in_thread
    def send(self, data):
        try:
            self.client.sendto(data, self.addr)
            response = self.client.recv(PACKET_SIZE)
            self.responses = response
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

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(self.addr)

    def handle_data(self, data: bytes) -> bytes:
        identification = data[0].to_bytes(1, 'little')
        if identification == b'\x00':
            identification = IOTA()
            return identification
        else:
            location = data[1:3]
            color = data[3:6]
            direction = data[6]
            self.all_players[identification] = data[1:]
            return self.format_all_players()

    def format_all_players(self) -> bytes:
        players = self.all_players
        response = b''
        for id in players.keys():
            response += id
            response += players[id]
        return response

    def run(self):
        print("server is listening...\n")
        while True:
            try:
                response, address = self.sock.recvfrom(PACKET_SIZE)
                if address not in self.addresses:
                    self.addresses.append(address)
                    print(f"new connection from {address}")
                    self.sock.sendto(IOTA(), address)

                print(response)
            except Exception as e:
                self.sock.close()
                print("error handled succesfully")
                print(e)
                break
        exit(1)

