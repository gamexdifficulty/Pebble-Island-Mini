from frostlight_engine import *
from typing import TYPE_CHECKING
from data.classes.animation import Animation, AnimationEvent

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
        self.can_be_deleted = False
        
        self.animation_state = "idle"
        self.fishing_state = "casting"
        self.animation = Animation(self.game)
        self.animation.register("idle",1,[Sprite("player_idle.png")])
        self.animation.register("fishing",1,[Sprite("player_idle.png")])
        self.animation.register("walk",0.15,[Sprite("player_walk_1.png"),
                                          Sprite("player_walk_2.png")])
        
        self.fishing_casting_animation = AnimationEvent(self.game, 0.6,[Sprite("rod_1.png"), Sprite("rod_2.png"), Sprite("rod_3.png"), Sprite("rod_4.png")], self.start_fishing)
        self.fishing_fishing_animation_sprite = Sprite("rod_5.png")
        self.fishing_pulling_animation = AnimationEvent(self.game, 0.6,[Sprite("rod_4.png"), Sprite("rod_3.png"), Sprite("rod_2.png"), Sprite("rod_1.png")], self.stop_fishing)
        
    def update(self):
        if self.alpha != 1.0 and not self.can_be_deleted:
            self.alpha = min(1,self.alpha+self.game.delta_time*0.75)
            
        if self.can_be_deleted:
            self.alpha = max(0.0,self.alpha-self.game.delta_time*0.75)
      
        if self.can_be_controlled:
            if self.game.input.get("fish"):
                if self.animation_state != "fishing":
                    self.fishing_state = "casting"
                    self.animation_state = "fishing"
                else:
                    if self.fishing_state == "fishing":
                        self.fishing_state = "pulling"
                        self.animation_state = "idle"
                        self.game.island.fishing_manager.pulling_in()

            if self.animation_state != "fishing" and self.fishing_state != "pulling" and self.fishing_state != "fishing" and not self.game.island.catch_book.opened:
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

        if self.fishing_state == "casting" and self.animation_state == "fishing":
            self.fishing_casting_animation.update()

        if self.animation_state != "fishing" and self.fishing_state != "casting":
            self.fishing_state = "pulling"

        if self.fishing_state == "pulling":
            self.fishing_pulling_animation.update()

    def draw(self):
        sprite = self.animation.get(self.animation_state)
        sprite.flipped = self.flipped
        sprite.alpha = self.alpha
        self.game.window.render(sprite, [int(self.x),int(self.y)])
        if self.fishing_state == "casting" and self.animation_state == "fishing":
            rod_sprite = self.fishing_casting_animation.get()
            rod_sprite.flipped = self.flipped
            rod_sprite.alpha = self.alpha
            offset_x = -2
            self.game.window.render(rod_sprite, [int(self.x)+offset_x,int(self.y)-4])
        elif self.fishing_state == "fishing":
            self.fishing_fishing_animation_sprite.flipped = self.flipped
            self.fishing_fishing_animation_sprite.alpha = self.alpha
            offset_x = -2
            self.game.window.render(self.fishing_fishing_animation_sprite, [int(self.x)+offset_x,int(self.y)-4])
        elif self.fishing_state == "pulling":
            rod_sprite = self.fishing_pulling_animation.get()
            rod_sprite.flipped = self.flipped
            rod_sprite.alpha = self.alpha
            offset_x = -2
            self.game.window.render(rod_sprite, [int(self.x)+offset_x,int(self.y)-4])

    def start_fishing(self):
        self.fishing_state = "fishing"
        if self.can_be_controlled:
            self.game.island.fishing_manager.start_fishing()

    def stop_fishing(self):
        self.fishing_state = "casting"
        if self.animation_state == "fishing":
            self.animation_state = "idle"