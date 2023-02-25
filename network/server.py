import socket
from packet import *
from dataclasses import dataclass
from typing import Tuple
from datetime import datetime, timedelta
import time
import threading

HOST = 'localhost'
PORT = 5555

@dataclass
class PlayerInfo:
    id: int
    address: Tuple[str, int]
    name: str
    last_packet_time: float = 0.0

class Server:
    def __init__(self, host, port) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = host
        self.port = port
        self.players: dict[int, PlayerInfo] = {}
        self.IOTA = 0
        self.timeout = 10

    def broadcast(self, packet: Packet):
        for player in self.players.copy().values():
            player.last_packet_time = datetime.now()
            self.sock.sendto(packet.serialize(), player.address)

    def check_timeouts(self):
        now = datetime.now()
        for player in self.players.copy().values():
            if now - player.last_packet_time > timedelta(seconds=self.timeout):
                print(player.name.decode(), "has timed out")
                del self.players[player.id]
                self.sock.sendto(Packet(PacketType.DISCONNECT, 0, PayloadFormat.DISCONNECT_REASON.pack(DisconnectReason.TIMEOUT)).serialize(), player.address)
    
    def handle_request(self, data, client_address):
            packet = Packet.deserialize(data)
            response_packet = Packet(PacketType.KEEP_ALIVE, packet.sequence_number, PayloadFormat.TIME.pack(time.time()))

            if packet.packet_type == PacketType.JOIN_REQUEST:
                requested_name = PayloadFormat.JOIN_REQUEST.unpack(packet.payload)[0]
                print("new player tried to connect with name:", requested_name.decode())
                #player_names = [player.name for player in self.players.values()]
                player_names = ["banned"]
                if requested_name not in player_names:
                    self.IOTA += 1
                    for player in self.players.values():
                        self.sock.sendto(Packet(PacketType.NEW_PLAYER, 0, PayloadFormat.NEW_PLAYER.pack(requested_name, player.id)).serialize(), player.address)
                        self.sock.sendto(Packet(PacketType.NAME, packet.sequence_number, PayloadFormat.NAME.pack(player.name, player.id)).serialize(), client_address)

                    self.players[self.IOTA] = PlayerInfo(self.IOTA, client_address, requested_name, datetime.now())
                    response_packet = Packet(PacketType.JOIN_RESPONSE, packet.sequence_number, PayloadFormat.JOIN_RESPONSE.pack(JoinResponses.ACCEPTED, self.IOTA))
                else:
                    response_packet = Packet(PacketType.JOIN_RESPONSE, packet.sequence_number, PayloadFormat.JOIN_RESPONSE.pack(JoinResponses.DENIED, 0))
            

            if packet.packet_type == PacketType.DISCONNECT:
                for player in self.players.copy().values():
                    if player.address == client_address:
                        del self.players[player.id]
                        print(player.name.decode(), "has disconnected")
                        reason = PayloadFormat.DISCONNECT_REASON.unpack(packet.payload)[0]
                        packet = Packet(PacketType.PLAYER_DISCONNECTED, 0, PayloadFormat.PLAYER_DISCONNECTED.pack(player.id, reason))
                        self.broadcast(packet)


            if packet.packet_type == PacketType.PLAYER_POSITION:
                packet = Packet(PacketType.PLAYER_POSITION, 0, packet.payload)
                self.broadcast(packet)

            response_packet_data = response_packet.serialize()


            self.check_timeouts()
            self.sock.sendto(response_packet_data, client_address)

    def run(self):
        self.sock.bind((self.host, self.port))
        print("starting server...")
        while True:
            data, client_address = self.sock.recvfrom(1024)  # 1024 is the buffer size

            threading.Thread(target=self.handle_request, args=(data, client_address)).start()

           

if __name__ == "__main__":
    s = Server("0.0.0.0", PORT)
    s.run()