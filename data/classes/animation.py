import time
from frostlight_engine import *
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import Game
    
class Animation:
    def __init__(self, game:"Game"):
        self.game = game
        self.config = {}
        
        self.start_time = time.time()

    def register(self, state:str, time:float, sprites:list):
        self.config[state] = {"duration":time, "count":len(sprites), "sprites":sprites}

    def get(self, state) -> int:
        elapsed = (time.time() - self.start_time) % self.config[state]["duration"]
        frame_time = self.config[state]["duration"] / self.config[state]["count"]
        frame_index = int(elapsed / frame_time)
        return self.config[state]["sprites"][frame_index]
    
class AnimationEvent:
    def __init__(self, game:"Game", time:float, sprites:list, callback):
        self.game = game
        self.config = {}

        self.index = 0
        self.timer = 0
        self.callback = callback
        
        self.config = {"duration":time, "count":len(sprites), "sprites":sprites}
        
    def get(self) -> int:
        return self.config["sprites"][self.index]
    
    def update(self):
        self.timer += self.game.delta_time
        frame_time = self.config["duration"] / self.config["count"]
        self.index = min(int(self.timer / frame_time), self.config["count"]-1)
        if self.timer > self.config["duration"]:
            self.timer = 0
            self.callback()
        