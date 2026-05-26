import time
from frostlight_engine import *
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import Game
    
from data.classes.animation import Animation, AnimationEvent
    
class Campfire:
    def __init__(self,game:"Game"):
        self.game = game
        
        self.campfire_state = "loop"
        self.campfire_off_sprite = Sprite("campfire_off.png")
        self.campfire_animation_on = AnimationEvent(self.game,0.4, callback=self.loop_campfire,sprites=
                                                    [
                                                        Sprite("campfire_start_1.png"),
                                                        Sprite("campfire_start_2.png"),
                                                        Sprite("campfire_start_3.png"),
                                                    ]
                                                    )
        
        self.campfire_animation_off = AnimationEvent(self.game,0.4, callback=self.extinguish_campfire,sprites=
                                                    [
                                                        Sprite("campfire_start_3.png"),
                                                        Sprite("campfire_start_2.png"),
                                                        Sprite("campfire_start_1.png"),
                                                    ]
                                                    )
        
        self.campfire_animation = Animation(self.game)
        self.campfire_animation.register("loop", 1.5, [
            Sprite("campfire_loop_1.png"),
            Sprite("campfire_loop_2.png"),
            Sprite("campfire_loop_3.png"),
            Sprite("campfire_loop_4.png"),
            Sprite("campfire_loop_5.png"),
            Sprite("campfire_loop_6.png"),
            Sprite("campfire_loop_7.png"),
            Sprite("campfire_loop_8.png"),
            Sprite("campfire_loop_9.png"),
            Sprite("campfire_loop_10.png"),
            Sprite("campfire_loop_11.png"),
        ])
        
        self.pos = [136,117]
    
    def update(self):
        if self.campfire_state == "light":
            self.campfire_animation_on.update()
        elif self.campfire_state == "extinguish":
            self.campfire_animation_off.update()
        elif self.campfire_state == "off":
            if self.game.gameManager.time >= 1800:
                self.campfire_state = "light"
        elif self.campfire_state == "loop":
            if self.game.gameManager.time >= 600 and self.game.gameManager.time < 1800:
                self.campfire_state = "extinguish"
    
    def draw(self):      
        if self.campfire_state == "light":
            self.game.window.render(self.campfire_animation_on.get(), self.pos)
        elif self.campfire_state == "extinguish":
            self.game.window.render(self.campfire_animation_off.get(), self.pos)
        elif self.campfire_state == "loop":
            self.game.window.render(self.campfire_animation.get("loop"), self.pos)
        else:
            self.game.window.render(self.campfire_off_sprite, self.pos)
    
    def light_campfire(self):
        self.campfire_state = "light"
    
    def extinguish_campfire(self):
        self.campfire_state = "off"
        
    def loop_campfire(self):
        self.campfire_state = "loop"