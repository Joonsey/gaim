import socket
from network.packet import *
import random, threading
from dataclasses import dataclass

@dataclass
class Player:
    id: int
    name: str = ""
    position: tuple[int, int] = (0,0)
    state: str = ""

PORT = 5555
HOST = "0.0.0.0"

addr = (HOST, PORT)

class Client:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = host
        self.port = port
        self.addr = (host, port)
        self.sequence_number = 0
        self.player_name = ""
        self.players : list[Player] = []
        self.id = 0
        self.die = False
        self.dead = False
    
    def update_player(self, player_id, **kwargs):
        for player in self.players:
            if player.id == player_id:
                for key, value in kwargs.items():
                    setattr(player, key, value)
                break
        else:
            # player not found, create new player object
            player = Player(id=player_id, **kwargs)
            self.players.append(player)
    
    def remove_player(self, player_id):
        player_to_remove = None
        for player in self.players:
            if player.id == player_id:
                player_to_remove = player

        if player_to_remove:
            self.players.remove(player_to_remove)

    def start(self):
        thread = threading.Thread(target=self.run)
        thread.start()

    def stop(self):
        self.die = True

    def broadcast_position(self, position: tuple[int, int]):
        packet = Packet(PacketType.PLAYER_POSITION, self.sequence_number, PayloadFormat.PLAYER_POSITION.pack(self.id, position[0], position[1]))
        self.sock.sendto(packet.serialize(), (self.host, self.port))

    def run(self):
        self.sock.sendto(Packet(PacketType.JOIN_REQUEST, self.sequence_number, PayloadFormat.JOIN_REQUEST.pack(self.player_name.encode())).serialize(), (self.host, self.port))
        self.sequence_number  += 1

        try:
            while not self.dead:
                data, addr = self.sock.recvfrom(1024)
                packet = Packet.deserialize(data)

                if packet.packet_type == PacketType.JOIN_RESPONSE:
                    #NOTE WHEN UNPACKING IT ALWAYS RETURNS A TUPLE
                    response, id = PayloadFormat.JOIN_RESPONSE.unpack(packet.payload)
                    if response == JoinResponses.ACCEPTED:
                        self.id = id
                        print("Join request accepted")
                    elif response == JoinResponses.DENIED:
                        print("Join request denied sadge")
                        return
                
                elif packet.packet_type == PacketType.NEW_PLAYER:
                    name, id = PayloadFormat.NEW_PLAYER.unpack(packet.payload)
                    self.update_player(id, name=name.decode("utf-8"))
                    print("new player connected!")

                elif packet.packet_type == PacketType.NAME:
                    name, id = PayloadFormat.NEW_PLAYER.unpack(packet.payload)
                    print(name)
                    self.update_player(id, name=name.decode("utf-8"))
                
                elif packet.packet_type == PacketType.PLAYER_DISCONNECTED:
                    id, reason = PayloadFormat.PLAYER_DISCONNECTED.unpack(packet.payload)
                    self.remove_player(id)

                elif packet.packet_type == PacketType.DISCONNECT:
                    reason = PayloadFormat.DISCONNECT_REASON.unpack(packet.payload)[0]
                    print("exited due to:", reason)
                    self.die = True
                
                elif packet.packet_type == PacketType.PLAYER_POSITION:
                    id, x, y = PayloadFormat.PLAYER_POSITION.unpack(packet.payload)
                    self.update_player(id, position=(x,y))

                if self.die:
                    self.sock.sendto(Packet(PacketType.DISCONNECT, self.sequence_number, PayloadFormat.DISCONNECT_REASON.pack(DisconnectReason.EXPECTED)).serialize(), (self.host, self.port))
                    self.dead = True

        except Exception as e:
            self.sock.sendto(Packet(PacketType.DISCONNECT, self.sequence_number, PayloadFormat.DISCONNECT_REASON.pack(DisconnectReason.UNEXPECTED)).serialize(), (self.host, self.port))
            raise e 


if __name__ == "__main__":
    name = input()
    client = Client(HOST,  PORT)
    client.player_name = name
    thread = threading.Thread(target=client.run, daemon=True)
    thread.run()
    
