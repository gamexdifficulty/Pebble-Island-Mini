import struct
import socket
import threading
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from server import GameServer

from data.classes.packets import *

class Client():
    def __init__(self,game:"GameServer",connection:socket.socket,address:list,sessionID:str):
        self.game = game
        self.connected = True
        self.socket = connection
        self.address = address
        
        self.sessionid = sessionID
        self.x = 0
        self.y = 0
        self.animation = "idle"
        self.flipped = False
        
        self.packet_map = {
            0:self.getQuit,
            1:self.getJoinRequest,
            3:self.getPlayerUpdate
        }
        
        threading.Thread(target=self.receive).start()
        
    def send(self,packet:Packet):
        if self.connected:
            threading.Thread(target=self.send_data,args=(packet,)).start()

    def send_data(self,packet:Packet):
        try:
            self.socket.sendall(packet.to_bytes())
        except Exception as e:
            self.close()
            print(f'Error while sending data: {self.address[0]}:{self.address[1]}|{packet}|{e}')
        
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
                    print("Unknown packet:", packet_id)
                    continue

                packet = packet_cls.from_bytes(packet_data)
                handler = self.packet_map.get(packet_id)

                if handler:
                    handler(packet)
                else:
                    print(f"No handler for packet {packet_id}")

        except Exception as e:
            print("Receive error:", e)
        finally:
            self.close()
            
    def getQuit(self,packet:PacketQuit):
        self.close()
            
    def getJoinRequest(self, packet:PacketJoinRequest):
        print(f"{self.sessionid} joined the server")
        self.send(PacketJoinConfirm(self.sessionid))
        
    def getPlayerUpdate(self, packet:PacketUpdatePlayer):
        self.x = packet.x        
        self.y = packet.y
        self.animation = packet.animation
        self.flipped = packet.flipped
        
        
        if self.x < 110 or self.x > 202 or self.y < 115 or self.y > 119:
            self.send(PacketQuit())
            self.close()
                
    def sendPlayerListUpdate(self, packet:PacketUpdatePlayerList):
        self.send(packet)
    
    def close(self):
        if not self.connected:
            return
        self.connected = False
        try:
            self.socket.close()
        except:
            pass
        print(f"{self.sessionid} disconnected")