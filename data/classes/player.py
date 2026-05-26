from frostlight_engine import *
from typing import TYPE_CHECKING
from data.classes.animation import Animation

if TYPE_CHECKING:
    from main import Game

class Player:
    def __init__(self, game:"Game", can_be_controlled=False):
        self.game = game
        self.x = 177
        self.y = 117
        self.target_x = self.x
        self.target_y = self.y
        self.id = None
        self.can_be_controlled = can_be_controlled
        self.flipped = False
        self.alpha = 0.0
        
        self.animation_state = "idle"
        self.animation = Animation(self.game)
        self.animation.register("idle",1,[Sprite("player_idle.png")])
        self.animation.register("walk",0.15,[Sprite("player_walk_1.png"),
                                          Sprite("player_walk_2.png")])
        
    def update(self):
        if self.alpha != 1.0:
            self.alpha = min(1,self.alpha+self.game.delta_time*0.75)
      
        if self.can_be_controlled:
            direction = self.game.input.get("right")-self.game.input.get("left")
            self.x = min(200,max(112,self.x + direction*self.game.delta_time*25))
            if direction == 1:
                self.flipped = False
                self.animation_state = "walk"
            elif direction == -1:
                self.flipped = True
                self.animation_state = "walk"
            else:
                self.animation_state = "idle"
        else:
            # Network movement
            smoothing = 20
            self.x += (self.target_x - self.x) * min(smoothing * self.game.delta_time, 1)
            self.y = self.target_y

    def draw(self):
        sprite = self.animation.get(self.animation_state)
        sprite.flipped = self.flipped
        sprite.alpha = self.alpha
        self.game.window.render(sprite, [int(self.x),int(self.y)])