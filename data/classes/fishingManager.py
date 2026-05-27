import math
import random
from frostlight_engine import *
from typing import TYPE_CHECKING

from data.classes.catchBook import RARITY_WEIGHTS, FISH_DATABASE

if TYPE_CHECKING:
    from main import Game

class FishingManager:
    def __init__(self, game:"Game"):
        self.game = game
        self.fishing = False
        self.hit_water = False
        self.start_time = [0,0]
        self.biting_wait_time = 0
        
        self.bobber_sprite = Sprite("bobber.png")
        self.bobber_pos = [0,0]

        self.fish_sprites = [
            Sprite("fish.png")
        ]

        self.flying_fish = None
        self.current_fish = None
        self.fish_biting = False
        self.bite_particle_timer = 0
        self.biting_hold_time = 0.0
        self.biting_hold_initial_time = 0.0

    def start_fishing(self):
        self.bobber_sprite.alpha = 1.0
        self.fishing = True
        self.start_time = [self.game.gameManager.time, self.game.gameManager.day]
        self.bobber_pos = [self.game.player.x-7+(1-(self.game.player.flipped))*17, self.game.player.y]
        
    def pulling_in(self):
        if self.fish_biting:
            self.pull_in_fish()
            self.catch_fish()
        self.stop_fishing()

    def stop_fishing(self):
        self.fish_biting = False
        self.hit_water = False
        self.fishing = False
        self.bobber_pos = [0,0]

    def update(self):
        self.calculate_bobber_position()
        self.update_flying_fish()
        self.update_biting_particles()
        self.biting_wait_time -= self.game.delta_time
        if self.fishing and self.hit_water and self.biting_wait_time <= 0 and not self.fish_biting:

            fish_data = self.choose_fish(self.game.gameManager.time, self.game.gameManager.day, int((self.game.gameManager.weather_value + 1) * 5))

            if fish_data:
                fish = fish_data
                self.current_fish = fish

                self.fish_biting = True
                self.biting_hold_time = fish["biting_hold_time"]
                self.biting_hold_initial_time = self.biting_hold_time
            
        if self.fish_biting:
            self.biting_hold_time -= self.game.delta_time
            self.bobber_sprite.alpha = max(0.0, self.biting_hold_time / self.biting_hold_initial_time)
            
            if self.biting_hold_time < -0.3:
                self.game.player.animation_state = "idle"
                self.current_fish = None
                self.stop_fishing()
            
    def draw(self):
        if self.flying_fish:
            self.game.window.render(self.flying_fish["sprite"], self.flying_fish["pos"])

        if self.fishing:
            if self.fish_biting:
                self.game.window.render(self.bobber_sprite, [self.bobber_pos[0], self.bobber_pos[1]+ 1 + math.sin((time.time()*20) % 100)])
            else:
                self.game.window.render(self.bobber_sprite, self.bobber_pos)
                
    def calculate_bobber_position(self):
        canvas_w, canvas_h = self.game.window.canvas_size
        sprite_w, sprite_h = 288, 148
        sprite_left = (canvas_w - sprite_w) // 2
        sprite_top = (canvas_h - sprite_h) // 2

        bobber_x = self.bobber_pos[0]
        uvs_x = (bobber_x - sprite_left) / sprite_w
        uvs_x = max(0.0, min(uvs_x, 1.0))

        uTime = (time.time() % 1000) / 3.0
        waterLevel = 0.2
        amplitude = 0.0625
        
        wave_up_down_2 = math.sin(uTime) * 0.4
        wave2_1 = math.sin(uvs_x * 20.0 + (uTime) * 2.0)
        wave2_2 = math.cos(uvs_x * 40.0 + (uTime) * 0.5)
        combined_2 = (wave_up_down_2 * 2.0 + wave2_1 + wave2_2)
        waveY_2 = 0.85 + combined_2 * amplitude

        y = waveY_2 * waterLevel
        uvs_y = 1.0 - y
        wave_top = sprite_top + uvs_y * sprite_h - 4

        self.bobber_pos[1] = min(self.bobber_pos[1] + self.game.delta_time*15, wave_top)
        if not self.hit_water and self.bobber_pos[1] >= wave_top:
            self.hit_water = True
            
            # wait time until bite
            self.biting_wait_time = random.randint(3,20)
            for _ in range(6):
                side = random.choice([-1, 1])

                pos = [self.bobber_pos[0] + random.randint(0, 4),self.bobber_pos[1]+2]
                vel = [side * random.randint(5, 18), -random.randint(8, 20)]
                self.game.island.particle_manager.spawn_particle(2,pos,[0, 0],vel, 0.45, flipped=(side < 0))

    def pull_in_fish(self):
        start_x = self.bobber_pos[0]
        start_y = self.bobber_pos[1]

        end_x = self.game.player.x+1+1-self.game.player.flipped
        end_y = self.game.player.y

        peak_height = 25

        control_x = (start_x + end_x) / 2
        control_y = min(start_y, end_y) - peak_height

        rarity = {"common":0,"rare":1,"very rare":2,"legendary":3}[self.current_fish["rarity"]]
        self.flying_fish = {
            "sprite": [
                    Sprite("fish.png"),
                    Sprite("rare_fish.png"),
                    Sprite("very_rare_fish.png"),
                    Sprite("legendary_fish.png")
                ][rarity],

            "start": [start_x, start_y],
            "control": [control_x, control_y],
            "end": [end_x, end_y],

            "t": 0.0,
            "speed": 1.0,

            "pos": [start_x, start_y]
        }

    def update_biting_particles(self):
        if not self.fish_biting:
            return

        self.bite_particle_timer += self.game.delta_time

        if self.bite_particle_timer >= 0.08:
            self.bite_particle_timer = 0
            side = random.choice([-1, 1])
            
            pos = [self.bobber_pos[0] + side * random.randint(0, 6),self.bobber_pos[1]]
            vel = [side * random.randint(3, 10), -random.randint(4, 12)]
            
            self.game.island.particle_manager.spawn_particle(2, pos, [0, 0], vel,0.35,flipped=(side < 0))

    def update_flying_fish(self):
        if not self.flying_fish:
            return

        fish = self.flying_fish
        fish["t"] += self.game.delta_time * fish["speed"]
        t = min(fish["t"], 1.0)

        x0, y0 = fish["start"]
        x1, y1 = fish["control"]
        x2, y2 = fish["end"]

        x = ((1 - t) ** 2) * x0 + 2 * (1 - t) * t * x1 + (t ** 2) * x2
        y = ((1 - t) ** 2) * y0 + 2 * (1 - t) * t * y1 + (t ** 2) * y2

        fish["pos"] = [x, y]

        dx = 2 * (1 - t) * (x1 - x0) + 2 * t * (x2 - x1)
        dy = 2 * (1 - t) * (y1 - y0) + 2 * t * (y2 - y1)

        angle = math.degrees(math.atan2(dy, dx))
        fish["sprite"].rotation = angle

        if t >= 1.0:
            self.flying_fish = None
            
    def time_in_range(self, current, start, end):
        if start <= end:
            return start <= current <= end
        return current >= start or current <= end


    def get_available_fish(self, current_time, current_day, current_wind):
        available = []

        for fish_id, fish in FISH_DATABASE.items():
            if not self.time_in_range(current_time, fish["time"][0], fish["time"][1]):
                continue
            if not (fish["day"][0] <= current_day <= fish["day"][1]):
                continue
            if not (fish["wind"][0] <= current_wind <= fish["wind"][1]):
                continue

            available.append((fish_id, fish))
        return available
            
    def choose_fish(self, current_time, current_day, current_wind):
        fish_pool = self.get_available_fish(current_time, current_day, current_wind)

        if not fish_pool:
            return None

        weighted = []

        for fish_id, fish in fish_pool:
            weight = RARITY_WEIGHTS[fish["rarity"]]
            weighted.extend([fish] * weight)

        return random.choice(weighted)
    
    def catch_fish(self):
        if not self.current_fish:
            return

        print(f'Caught: {self.current_fish["name"]}')