import time
import random
from frostlight_engine import *
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import Game

from data.classes.campfire import Campfire
from data.classes.grass import Grass
from data.classes.sky import Sky
from data.classes.particle import ParticleManager
class Island:
    def __init__(self, game:"Game"):
        self.game = game
        
        self.house_particle_timer = 0
        self.campfire_particle_timer = 0
        
        self.campfire = Campfire(self.game)
        self.grass = Grass(self.game)
        self.sky = Sky(self.game)
        self.particle_manager = ParticleManager(self.game)
        
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
        self.sky.update()
        self.particle_manager.update()
        self.water_sprite.set_custom_uniforms("uTime",time.time() % 1000)
        
        self.house_particle_timer = max(self.house_particle_timer-self.game.delta_time, 0.0)
        if self.house_particle_timer <= 0:
            self.particle_manager.spawn_particle(1, [158,90], [5,1], [0, -4], random.randint(3,6))
            self.house_particle_timer = random.randint(10,25)/10
        
        if self.game.gameManager.time > 1800 or self.game.gameManager.time < 600:
            self.campfire_particle_timer = max(self.campfire_particle_timer-self.game.delta_time, 0.0)
            if self.campfire_particle_timer <= 0:
                self.particle_manager.spawn_particle(1, [135,111], [8,2], [0, -4], random.randint(3,6))
                self.campfire_particle_timer = random.randint(8,12)/10

    def draw(self):
        self.sky.draw()
        self.game.window.render(self.island_sprite, [112,125])
        self.campfire.draw()
        self.game.window.render(self.house_sprite, [160,97])
        self.game.window.render(self.water_sprite, [16,16])
        self.game.player_manager.draw()
        self.particle_manager.draw()
        self.grass.draw()
        self.game.window.render(self.border_sprite, [0,0])

