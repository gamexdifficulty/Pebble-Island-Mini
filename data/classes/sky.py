import random
from frostlight_engine import *
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import Game

class Sky:
    def __init__(self,game:"Game"):
        self.game = game
        self.sky_sprite = Sprite("sky.png")
        self.stars_sprite = Sprite("stars.png")

        self.clouds:list[Cloud] = [
            Cloud(self.game, 0, [32,22]),
            Cloud(self.game, 1, [80,25]),
            Cloud(self.game, 2, [130,27]),
            Cloud(self.game, 1, [190,31]),
            Cloud(self.game, 0, [250,24]),
        ]

        self.sky_sprite.set_custom_shader("sky.frag")

    def update(self):        
        # Sky
        if self.game.gameManager.time >= 1900:
            self.stars_sprite.alpha = min(1.0, ((self.game.gameManager.time-1900)/200))
        elif self.game.gameManager.time >= 600 and self.game.gameManager.time < 1900:
            self.stars_sprite.alpha = 1-min(1.0, ((self.game.gameManager.time-600)/100))
        else:
            self.stars_sprite.alpha = 1
            
        self.sky_sprite.set_custom_uniforms("uTime", self.game.gameManager.time)
            
        # Clouds
        weather_value = int((self.game.gameManager.weather_value + 1) * 5)
        num_clouds = int(3 + (weather_value/10)*7)

        CLOUD_WIDTH = 30
        SCREEN_WIDTH = 320

        spacing = (SCREEN_WIDTH + CLOUD_WIDTH) / num_clouds
        # print(spacing, num_clouds)

        if num_clouds > len(self.clouds):

            last_cloud = self.clouds[-1]

            required_distance = (
                spacing * random.uniform(0.8, 1.2)
            )

            if last_cloud.pos[0]+16 > required_distance:
                self.spawn_cloud()
                    
        for cloud in self.clouds.copy():
            cloud.update(max(weather_value/2,1))
            if cloud.can_be_deleted:
                self.clouds.remove(cloud)

    def draw(self):
        self.game.window.render(self.sky_sprite, [16,16])
        self.game.window.render(self.stars_sprite, [16,16])
        for cloud in self.clouds.copy():
            cloud.draw()

    def spawn_cloud(self):
        cloud = Cloud(self.game, random.randint(0,2), [-16,22+random.randint(0,12)])
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
        
        self.sprite.set_custom_shader("cloud.frag")

    def update(self, velocity):
        self.pos[0] += (velocity * 10/7) * self.game.delta_time
        if self.pos[0] > self.game.window.canvas_size[0]-16:
            self.can_be_deleted = True
            
        self.sprite.set_custom_uniforms("uTime", self.game.gameManager.time)

    def draw(self):
        self.game.window.render(self.sprite, self.pos)