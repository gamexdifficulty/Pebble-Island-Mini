import time
from frostlight_engine import *
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import Game
    
from data.classes.animation import Animation, AnimationEvent
    
class Grass:
    def __init__(self,game:"Game"):
        self.game = game
    
        self.grass_animation = Animation(self.game)
        self.grass_animation.register("loop", 2, [
            Sprite("grass_loop_1.png"),
            Sprite("grass_loop_2.png"),
            Sprite("grass_loop_3.png"),
            Sprite("grass_loop_4.png")
        ])
        
        self.pos = [113,119]
    
    def update(self):
        pass
    
    def draw(self):
        self.game.window.render(self.grass_animation.get("loop"), self.pos)
