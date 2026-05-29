import struct
import socket
import threading

from data.classes.packets import *
from frostlight_engine import *
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import Game

class NetworkManager:
    def __init__(self,game:"Game"):
        self.game = game
        
        self.connected = False
        self.address = ("frostlightgames.net", 50451)
        self.sessionID = ""

        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        
        self.packet_map = {
            0:self.getQuit,
            2:self.getJoinAccept,
            4:self.getUpdatePlayerList
        }
        
    def run(self):
        threading.Thread(target=self.loop,args=(),daemon=True).start()
        
    def send(self,packet:Packet):
        if not self.connected:
            return

        try:
            self.socket.sendall(packet.to_bytes())

        except Exception as e:
            self.game.logger.error("Send error")
            self.close()
        
    def recv_exact(self, size: int) -> bytes:
        data = b""
        while len(data) < size:
            chunk = self.socket.recv(size - len(data))
            if not chunk:
                raise ConnectionError("Disconnected")
            data += chunk
        return data
        
    def receive(self):
        try:
            while self.connected:
                raw_length = self.recv_exact(4)
                packet_length = struct.unpack("!I", raw_length)[0]
                body = self.recv_exact(packet_length)
                packet_id = struct.unpack("!H", body[:2])[0]
                packet_data = body[2:]
                packet_cls = PACKETS.get(packet_id)

                if packet_cls is None:
                    self.game.logger.error(f"Unknown packet: {packet_id}")
                    continue

                packet = packet_cls.from_bytes(packet_data)
                handler = self.packet_map.get(packet_id)

                if handler:
                    handler(packet)
                else:
                    self.game.logger.error(f"No handler for packet {packet_id}")

        except Exception as e:
            if type(e) != ConnectionError:
                self.game.logger.error("Receive error")
        finally:
            self.close()
    
    def getQuit(self,packet:PacketQuit):
        self.close()
        
    def send_quit(self):
        self.send(PacketQuit())
    
    def getJoinAccept(self,packet:PacketJoinConfirm):
        self.game.logger.info(f"Joined Server, go SessionID {packet.sessionID}")
        self.sessionID = packet.sessionID
    
    def getUpdatePlayerList(self, packet:PacketUpdatePlayerList):
        data = packet.players
        count = struct.unpack("!H", data[:2])[0]
        offset = 2

        player_dict = {}

        for i in range(count):
            session_length = struct.unpack("!H", data[offset:offset+2])[0]
            offset += 2

            session_id = struct.unpack(f"!{session_length}s", data[offset:offset+session_length])[0].decode("utf-8")
            offset += session_length

            x, y = struct.unpack("!hh", data[offset:offset+4])
            offset += 4

            anim_length = struct.unpack("!H", data[offset:offset+2])[0]
            offset += 2

            animation = struct.unpack(f"!{anim_length}s", data[offset:offset+anim_length])[0].decode("utf-8")
            offset += anim_length

            flip = struct.unpack("!?", data[offset:offset+1])[0]
            offset += 1

            if self.sessionID != session_id:
                player_dict[session_id] = [x, y, animation, flip]
            
        self.game.player_manager.update_player_list(player_dict)
        
    def loop(self):
        while self.game.running:
            while not self.connected and self.game.running:
                try:
                    self.socket.connect(self.address)
                    self.connected = True
                    threading.Thread(target=self.receive,daemon=True).start()
                    self.send(PacketJoinRequest())
                except Exception:
                    self.game.logger.error("Failed to connect to server")
                    time.sleep(1)

            clock = pygame.time.Clock()
            while self.connected:
                clock.tick(20)
                if self.sessionID != "":
                    player = self.game.player
                    self.send(PacketUpdatePlayer(int(player.x),int(player.y),player.animation_state,player.flipped))

            self.connected = False
    
    def close(self):
        self.sessionID = ""
        if not self.connected:
            return
        self.connected = False
        try:
            self.socket.close()
        except:
            pass
        self.game.logger.info("Disconnected from server")