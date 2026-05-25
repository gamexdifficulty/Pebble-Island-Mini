import time
from frostlight_engine import *
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import Game
    
class GameManager:
    def __init__(self,game:"Game"):
        self.game = game
        
        self.time = 0
        self.day = 1
    
    def update(self):
        self.time += 8*self.game.delta_time
        if self.time >= 2400:
            self.time -= 2400
            self.day += 1
            if self.day >= 31:
                self.day = 1
        print(self.time, self.day)
