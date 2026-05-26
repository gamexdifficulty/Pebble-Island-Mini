import time
import struct
import socket
import pygame
import threading

from data.classes.client import Client
from data.classes.packets import *

TICKSPEED = 20

import string
import secrets

def generate_uid(used_uids):
    for _ in range(100):
        new_uid = ""
        for _ in range(8):
            new_uid += secrets.choice(string.digits + string.ascii_lowercase)

        if new_uid not in used_uids:
            used_uids.add(new_uid)
            return new_uid

    raise Exception("Failed to generate UID")

class GameServer:
    def __init__(self):
        self.running = True
        self.delta_time = 1
        self.last_time = 1
        self.clock = pygame.time.Clock()
        
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        self.address = (socket.gethostbyname(socket.gethostname()),50451)
        self.socket.bind(self.address)

        self.clients: dict[str,Client] = {}
        self.client_lock = threading.Lock()
        self.used_uuids = set()
    
    def update(self):
        self.last_time = time.time()
        while self.running:
            self.clock.tick(TICKSPEED)

            self.delta_time = time.time()-self.last_time
            self.last_time = time.time()
            
            with self.client_lock:
                clients = list(self.clients.values())

            disconnected = []

            for client in clients:
                if not client.connected:
                    disconnected.append(client.sessionid)

            if disconnected:
                with self.client_lock:
                    for session_id in disconnected:
                        if session_id in self.clients:
                            del self.clients[session_id]
                            print(f"Removed client {session_id}")

            # refresh snapshot
            with self.client_lock:
                clients = list(self.clients.values())

            data = struct.pack("!H", len(clients))

            for player in clients:
                session_bytes = (player.sessionid.encode("utf-8"))
                animation_bytes = (player.animation.encode("utf-8"))
                data += struct.pack(
                    f"!H{len(session_bytes)}s"
                    f"hh"
                    f"H{len(animation_bytes)}s"
                    f"?",

                    len(session_bytes),
                    session_bytes,

                    int(player.x),
                    int(player.y),

                    len(animation_bytes),
                    animation_bytes,

                    player.flipped
                )
            packet = PacketUpdatePlayerList(data)

            for client in clients:
                if client.connected:
                    client.send(packet)
    
    def start(self):
        # starting socket and update loop
        print(f'[Starting server]')
        threading.Thread(target=self.update,daemon=True).start()
        self.socket.listen()
        print(f'Server listening on {self.address[0]}:{self.address[1]}')
        while self.running:
            try:
                # accepting new connections
                connection,address = self.socket.accept()
                print(f'New Client: {address[0]}:{address[1]}')
                session_id = generate_uid(self.used_uuids)
                client = Client(self,connection,address, session_id)
                with self.client_lock:
                    self.clients[session_id] = client
            except Exception as e:
                if self.running:
                    print(f"Error while listening for new connections: {e}")
                    self.stop()

    def stop(self):
        self.running = False
        try:
            self.socket.close()
        except:
            pass
    
if __name__ == "__main__":
    server = GameServer()
    server.start()