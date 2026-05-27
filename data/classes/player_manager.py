from frostlight_engine import *
from data.classes.player import Player
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import Game


class PlayerManager:

    def __init__(self, game: "Game"):

        self.game = game

        self.player_list = {}
        self.create_queue = {}
        
        self.player_indicator_sprite = Sprite("player_indicator.png")

    def update(self):
        for session_id in list(self.create_queue.keys()):

            data = self.create_queue[session_id]

            player = Player(self.game)

            player.id = session_id

            player.x = data[0]
            player.y = data[1]

            player.target_x = data[0]
            player.target_y = data[1]

            player.animation_state = data[2]
            player.flipped = data[3]

            self.player_list[session_id] = player

            del self.create_queue[session_id]

        for player in self.player_list.values():
            player.update()

        self.player_indicator_sprite.alpha = (50 + (math.sin(self.game.gameManager.time/2) + 1) * 50)/255

    def draw(self):
        for player in self.player_list.values():
            player.draw()
        
        if self.game.network_manager.connected:
            self.game.window.render(self.player_indicator_sprite,[int(self.game.player.x)+2,self.game.player.y-2])

    def get(self, session_id):
        return self.player_list.get(session_id)

    def update_player_list(self, data: dict):
        incoming_ids = set(data.keys())
        current_ids = set(self.player_list.keys())

        for session_id in incoming_ids:

            player_data = data[session_id]

            x = player_data[0]
            y = player_data[1]
            animation = player_data[2]
            flipped = player_data[3]

            # New player
            if session_id not in self.player_list:
                self.register_player(session_id, x, y, animation, flipped)

                continue

            # Existing player
            player = self.player_list[session_id]

            player.target_x = int(x)
            player.target_y = int(y)

            player.animation_state = animation
            player.flipped = flipped

        disconnected = current_ids - incoming_ids
        for session_id in disconnected:
            player = self.player_list[session_id]
            if not player.can_be_controlled:
                self.unregister_player(session_id)
                if self.player_list[session_id].alpha == 0.0:
                    del self.player_list[session_id]

    def register_player(self,session_id: str, x, y, animation, flipped):
        self.create_queue[session_id] = [x, y, animation, flipped]
        
    def unregister_player(self, session_id):
        if session_id in self.player_list:
            self.player_list[session_id].can_be_deleted = True