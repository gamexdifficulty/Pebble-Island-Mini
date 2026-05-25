import time
from frostlight_engine import *
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import Game

from data.classes.campfire import Campfire

class Island:
    def __init__(self, game:"Game"):
        self.game = game
        
        self.campfire = Campfire(self.game)
        
        self.border_sprite = Sprite("border.png")
        self.island_sprite = Sprite("island.png")
        self.house_sprite = Sprite("house.png")
        self.grass_sprite = Sprite("grass.png")
        self.sky_sprite = Sprite("sky.png")
        self.water_sprite = Sprite("water.png")
        
        self.water_sprite.set_custom_shader("water_wave.frag")

    def update(self):
        self.game.player_manager.update()
        self.campfire.update()
        self.water_sprite.set_custom_uniforms("uTime",time.time() % 1000)

    def draw(self):
        self.game.window.render(self.sky_sprite, [16,16])
        self.game.window.render(self.island_sprite, [112,125])
        self.campfire.draw()
        self.game.window.render(self.house_sprite, [160,97])
        self.game.window.render(self.water_sprite, [16,16])
        self.game.player_manager.draw()
        self.game.window.render(self.grass_sprite, [113,119])
        self.game.window.render(self.border_sprite, [0,0])
        
