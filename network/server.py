import socket
from packet import *
from dataclasses import dataclass
from typing import Tuple
from datetime import datetime, timedelta
import time
import json
import sys
import threading

HOST = "0.0.0.0"
PORT = 5555

@dataclass
class PlayerInfo:
    id: int
    address: Tuple[str, int]
    name: str
    last_packet_time: datetime = datetime.now()

@dataclass
class Enemy:
    id: int
    type: int
    position: Tuple[int, int]
    health: int = 100

    def to_dict(self):
        return {
            "id":self.id,
            "type":self.type,
            "position":self.position,
            "health":self.health,
        }
    
    def to_json(self):
        return json.dumps(self.to_dict())


class Server:
    def __init__(self, host, port) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = host
        self.port = port
        self.players: dict[int, PlayerInfo] = {}
        self.enemies: dict[int, Enemy] = {}
        self.IOTA = 0
        self.timeout = 10
        self.interval = 1000
        self.last_packet_time = datetime.now()

        self.enemies = {
            1 : Enemy(1, 0, (0,0), 100),
            2 : Enemy(2, 0, (0,0), 100),
            3 : Enemy(3, 0, (0,0), 100),
            4 : Enemy(4, 0, (0,0), 100),
            5 : Enemy(5, 0, (0,0), 100),
        }

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


        now = datetime.now()
        if now - self.last_packet_time > timedelta(microseconds=self.interval):
            enemy_status_packet = Packet(PacketType.ENEMY_STATUS, 0, json.dumps([enemy.to_dict() for enemy in self.enemies.values()]).encode())
            self.broadcast(enemy_status_packet)

        if packet.packet_type == PacketType.JOIN_REQUEST:
            requested_name = PayloadFormat.JOIN_REQUEST.unpack(packet.payload)[0].decode("utf-8")
            #player_names = [player.name for player in self.players.values()]
            player_names = ["banned"]
            if requested_name not in player_names:
                self.IOTA += 1
                for player in self.players.values():
                    self.sock.sendto(Packet(PacketType.NEW_PLAYER, 0, PayloadFormat.NEW_PLAYER.pack(requested_name, self.IOTA)).serialize(), player.address)
                    self.sock.sendto(Packet(PacketType.NAME, packet.sequence_number, PayloadFormat.NAME.pack(player.name, player.id)).serialize(), client_address)

                self.players[self.IOTA] = PlayerInfo(self.IOTA, client_address, requested_name, datetime.now())
                response_packet = Packet(PacketType.JOIN_RESPONSE, packet.sequence_number, PayloadFormat.JOIN_RESPONSE.pack(JoinResponses.ACCEPTED, self.IOTA))
                print(f"{requested_name} has connected!")
            else:
                response_packet = Packet(PacketType.JOIN_RESPONSE, packet.sequence_number, PayloadFormat.JOIN_RESPONSE.pack(JoinResponses.DENIED, 0))

        if packet.packet_type == PacketType.PLAYER_STATE_CHANGE:
            for player in self.players.copy().values():
                packet = Packet(PacketType.PLAYER_STATE_CHANGE, 0, packet.payload)
                self.broadcast(packet)

        if packet.packet_type == PacketType.DISCONNECT:
            for player in self.players.copy().values():
                if player.address == client_address:
                    del self.players[player.id]
                    print(player.name, "has disconnected")
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
        print(f"starting server...\nlistening on {(self.host, self.port)}")
        while True:
            data, client_address = self.sock.recvfrom(1024)  # 1024 is the buffer size

            threading.Thread(target=self.handle_request, args=(data, client_address)).start()

            

if __name__ == "__main__":
    if "-l" in sys.argv:
        HOST = "localhost"
    s = Server(HOST, PORT)
    s.run()
