import struct

class PacketType:
    JOIN_REQUEST = 1
    JOIN_RESPONSE = 2
    PLAYER_POSITION = 3
    PLAYER_ACTION = 4
    NEW_PLAYER = 5
    NAME = 5
    DISCONNECT = 6
    PLAYER_DISCONNECTED = 7
    KEEP_ALIVE = 8

class DisconnectReason:
    EXPECTED = 0
    UNEXPECTED = 1
    TIMEOUT = 2

class JoinResponses:
    ACCEPTED = 0
    DENIED = 1

class PayloadFormat:
    JOIN_REQUEST = struct.Struct('16s')
    JOIN_RESPONSE = struct.Struct('!II')
    NEW_PLAYER = struct.Struct('!16sI')
    NAME = struct.Struct('!16sI')
    PLAYER_POSITION = struct.Struct('!Idd')
    PLAYER_MOVEMENT = struct.Struct('!Idddd')
    PLAYER_CHAT_MESSAGE = struct.Struct('32s')
    PLAYER_HEALTH = struct.Struct('!H')
    PLAYER_SCORE = struct.Struct('!I')
    DISCONNECT_REASON = struct.Struct('!I')
    PLAYER_DISCONNECTED = struct.Struct('!II')
    TIME = struct.Struct('!d')

class Packet:
    HEADER_SIZE = struct.calcsize('IBII')
    MAGIC_NUMBER = 0xDEADBEEF

    def __init__(self, packet_type, sequence_number, payload):
        self.packet_type = packet_type
        self.sequence_number = sequence_number
        self.payload = payload

    def serialize(self):
        magic_number_bytes = struct.pack('I', self.MAGIC_NUMBER)
        packet_type_bytes = struct.pack('I', self.packet_type)
        sequence_number_bytes = struct.pack('I', self.sequence_number)
        payload_length_bytes = struct.pack('I', len(self.payload))

        headers = magic_number_bytes + packet_type_bytes + sequence_number_bytes + payload_length_bytes
        serialized_packet = headers + self.payload

        return serialized_packet

    @classmethod
    def deserialize(cls, serialized_data):
        if len(serialized_data) < Packet.HEADER_SIZE:
            raise ValueError("Invalid packet - packet is too short")

        magic_number, packet_type, sequence_number, payload_length = struct.unpack('IIII', serialized_data[:Packet.HEADER_SIZE])
        
        if magic_number != Packet.MAGIC_NUMBER:
            print("WARNING: magic number mis-match of packets. \npacket will be disqualified")
            return None
        payload = serialized_data[Packet.HEADER_SIZE: Packet.HEADER_SIZE+ payload_length]

        return Packet(packet_type, sequence_number, payload)