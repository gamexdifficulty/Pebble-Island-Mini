import time
import random
import opensimplex
from frostlight_engine import *
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import Game
    
SCALE = 0.0008

class Sky:
    def __init__(self,game:"Game"):
        self.game = game
        self.sky_sprite = Sprite("sky.png")

        opensimplex.seed(933673157426)

        self.clouds:list[Cloud] = [
            Cloud(self.game, 0, [30,22]),
            Cloud(self.game, 1, [80,25]),
            Cloud(self.game, 2, [130,27]),
            Cloud(self.game, 1, [190,31]),
            Cloud(self.game, 0, [250,24]),
        ]

        self.game.window.render(self.sky_sprite, [16,16])

    def update(self):
        val = opensimplex.noise2((self.game.gameManager.day*2400+self.game.gameManager.time)*SCALE,1*SCALE)
        val = int((val + 1) * 5)

        for cloud in self.clouds.copy():
            cloud.update(val)
            if cloud.can_be_deleted:
                self.clouds.remove(cloud)

        num_clouds = int(3 + (val/10)*7)

        print(num_clouds, len(self.clouds), val)

        if num_clouds > len(self.clouds):
            for i in range(num_clouds-len(self.clouds)):
                last_cloud = self.clouds[-1]
                if last_cloud.pos[0] > 16:
                    self.spawn_cloud()

    def draw(self):
        self.game.window.render(self.sky_sprite, [16,16])
        for cloud in self.clouds.copy():
            cloud.draw()

    def spawn_cloud(self):
        cloud = Cloud(self.game, random.randint(0,2), [-32,22+random.randint(0,12)])
        self.clouds.append(cloud)

class Cloud:
    def __init__(self, game:"Game", cloud_type, pos):
        self.game = game
        self.type = cloud_type
        self.pos = pos
        self.can_be_deleted = False

        self.sprite = [
            Sprite("cloud1.png"),
            Sprite("cloud2.png"),
            Sprite("cloud3.png"),
        ][self.type]

    def update(self, vel):
        self.pos[0] += (vel * 10/7) * self.game.delta_time
        if self.pos[0] > self.game.window.canvas_size[0]-16:
            self.can_be_deleted = True

    def draw(self):
        self.game.window.render(self.sprite, self.pos)