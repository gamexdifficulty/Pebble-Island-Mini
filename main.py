from frostlight_engine import *

from data.classes.island import Island
from data.classes.button import Button
from data.classes.player import Player
from data.classes.player_manager import PlayerManager
from data.classes.gameManager import GameManager

class Game(FrostlightEngine):
    def __init__(self):
        super().__init__(canvas_size=[320,180],fps_limit=165)
        self.running = True
        self.transition = False
        self.state = "menu"

        self.transition_unit = 1.0
        self.mouse_pos = [0,0]

        self.input.bind("left",KEYBOARD.LEFT,PRESSED)
        self.input.bind("left",KEYBOARD.A,PRESSED)
        self.input.bind("right",KEYBOARD.RIGHT,PRESSED)
        self.input.bind("right",KEYBOARD.D,PRESSED)

        self.input.bind("up",KEYBOARD.UP,PRESSED)
        self.input.bind("up",KEYBOARD.W,PRESSED)
        self.input.bind("down",KEYBOARD.DOWN,PRESSED)
        self.input.bind("down",KEYBOARD.S,PRESSED)

        self.input.bind("accept",MOUSE.LEFT,CLICKED)
        self.input.bind("accept",KEYBOARD.ENTER,PRESSED)
        
        self.input.bind("menu",KEYBOARD.ESCAPE,CLICKED)

        self.mouse_sprite = Sprite("mouse.png")

        self.multiplayer_button = Button(self, pos=[144,64], sprite="button-multiplayer.png", callback=self.button_multiplayer)
        self.singleplayer_button = Button(self, pos=[144,84], sprite="button-singleplayer.png", callback=self.button_singleplayer)
        self.leave_button = Button(self, pos=[144,104], sprite="button-leave.png", callback=self.button_quit)
        
        self.gameManager = GameManager(self)
        
        self.player = Player(self,True)
        self.island = Island(self)
        self.player_manager = PlayerManager(self)

        self.player_manager.player_list[None] = self.player
        
    def event_quit(self):
        self.running = False

    def begin_transition(self):
        self.transition = True
        
    def button_quit(self):
        self.running = False
        exit(0)
    
    def button_multiplayer(self):
        self.begin_transition()
    
    def button_singleplayer(self):
        self.begin_transition()
    
    def update(self):
        self.mouse_pos = [(self.input.mouse.position[0]/self.window.window_size[0])*self.window.canvas_size[0], 
                     (self.input.mouse.position[1]/self.window.window_size[1])*self.window.canvas_size[1]]
        
        if self.transition:
            self.transition_unit = max(0.0, self.transition_unit - 1.0*self.delta_time)
            if self.transition_unit == 0.0:
                self.state = "game"
                self.transition = False
                self.transition_unit = 1.0

        self.island.update()
        self.gameManager.update()

        if self.state == "menu":
            self.multiplayer_button.update(self.mouse_pos, self.transition_unit)
            self.singleplayer_button.update(self.mouse_pos, self.transition_unit)
            self.leave_button.update(self.mouse_pos, self.transition_unit)
            self.mouse_sprite.alpha = self.transition_unit
              
        if self.input.get("menu"):
            self.state = "menu"

    def draw(self):
        self.island.draw()

        if self.state == "menu":
            self.multiplayer_button.draw()
            self.singleplayer_button.draw()
            self.leave_button.draw()
            self.window.render(self.mouse_sprite, self.mouse_pos)

game = Game()
game.run()