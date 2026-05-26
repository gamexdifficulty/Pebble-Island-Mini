import opensimplex
from frostlight_engine import *
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import Game

SCALE = 0.0008

class GameManager:
    def __init__(self,game:"Game"):
        self.game = game
        
        self.weather_value = 0
        self.time = 500
        self.day = 1

        opensimplex.seed(933673157426)
        
    def update(self):
        self.weather_value = opensimplex.noise2((self.day*2400+self.time)*SCALE,1*SCALE)
        
        self.time += 8*self.game.delta_time
        if self.time >= 2400:
            self.time -= 2400
            self.day += 1
            if self.day >= 31:
                self.day = 1