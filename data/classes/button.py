from frostlight_engine import *
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import Game

class Button:
    def __init__(self, game:"Game", pos:list=[0,0], sprite:str="" ,callback=None):
        self.game = game
        self.pos = pos
        self.callback = callback

        self.sprite = Sprite(sprite)
        self.outline = Sprite("button-selected.png")
        self.selector = Sprite("button-selector.png")
        self.size = [32,16]
        self.mouse_pos = [0,0]
        self.selected = False
        self.alpha = 1.0

    def update(self, mouse_pos:list=[0,0], alpha:float=1):
        self.selected = False
        self.mouse_pos = mouse_pos
        if mouse_pos[0] > self.pos[0] and mouse_pos[0] < self.pos[0]+self.size[0] and mouse_pos[1] > self.pos[1] and mouse_pos[1] < self.pos[1]+self.size[1]:
            if alpha == 1.0:
                self.selected = True
                if self.game.input.get("accept"):
                    self.game.input.reset_key("accept")
                    if self.callback != None:
                        self.callback()

        self.sprite.alpha = alpha
        self.outline.alpha = alpha
        self.selector.alpha = alpha

    def draw(self):
        self.game.window.render(self.sprite, self.pos)
        if self.selected:
            self.game.window.render(self.outline, self.pos)
            self.game.window.render(self.selector, [self.pos[0]-6,self.pos[1]])