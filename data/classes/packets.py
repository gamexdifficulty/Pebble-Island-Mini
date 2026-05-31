import struct
import json
from dataclasses import dataclass, asdict

class Packet:
    PACKET_ID = -1

    def to_bytes(self) -> bytes:
        data = json.dumps(asdict(self)).encode("utf-8")
        header = struct.pack("!IH", len(data) + 2, self.PACKET_ID)
        return header + data

    @classmethod
    def from_bytes(cls, data: bytes):
        values = json.loads(data.decode("utf-8"))
        return cls(**values)
    
@dataclass
class PacketQuit(Packet):
    PACKET_ID = 0

    ping = 0

@dataclass
class PacketJoinRequest(Packet):
    PACKET_ID = 1

    protocolVersion = 1
    
@dataclass
class PacketJoinConfirm(Packet):
    PACKET_ID = 2

    sessionID: str
    
@dataclass
class PacketUpdatePlayer(Packet):
    PACKET_ID = 3

    x: int
    y: int
    animation: str
    flipped: bool
    
@dataclass
class PacketUpdatePlayerList(Packet):
    PACKET_ID = 4

    players: bytes

    def to_bytes(self):

        header = struct.pack(
            "!IH",
            len(self.players) + 2,
            self.PACKET_ID
        )

        return header + self.players

    @classmethod
    def from_bytes(cls, data: bytes):
        return cls(data)

PACKETS = {
    PacketQuit.PACKET_ID: PacketQuit,
    PacketJoinRequest.PACKET_ID: PacketJoinRequest,
    PacketJoinConfirm.PACKET_ID: PacketJoinConfirm,
    PacketUpdatePlayer.PACKET_ID: PacketUpdatePlayer,
    PacketUpdatePlayerList.PACKET_ID: PacketUpdatePlayerList
}
