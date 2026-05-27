from frostlight_engine import *

from data.classes.island import Island
from data.classes.button import Button
from data.classes.player import Player
from data.classes.player_manager import PlayerManager
from data.classes.networkManager import NetworkManager
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
        
        self.input.bind("book_left",KEYBOARD.LEFT,CLICKED)
        self.input.bind("book_left",KEYBOARD.A,CLICKED)
        self.input.bind("book_right",KEYBOARD.RIGHT,CLICKED)
        self.input.bind("book_right",KEYBOARD.D,CLICKED)
        self.input.bind("book_close",KEYBOARD.DOWN,CLICKED)
        self.input.bind("book_close",KEYBOARD.S,CLICKED)
        
        self.input.bind("ui_left",KEYBOARD.J,CLICKED)
        self.input.bind("ui_right",KEYBOARD.L,CLICKED)
        self.input.bind("ui_up",KEYBOARD.I,CLICKED)
        self.input.bind("ui_down",KEYBOARD.K,CLICKED)

        self.input.bind("up",KEYBOARD.UP,PRESSED)
        self.input.bind("up",KEYBOARD.W,PRESSED)
        self.input.bind("down",KEYBOARD.DOWN,PRESSED)
        self.input.bind("down",KEYBOARD.S,PRESSED)
        
        self.input.bind("fish",KEYBOARD.SPACE,CLICKED)

        self.input.bind("accept",MOUSE.LEFT,CLICKED)
        self.input.bind("accept",KEYBOARD.ENTER,CLICKED)
        self.input.bind("accept",KEYBOARD.UP,CLICKED)
        self.input.bind("accept",KEYBOARD.W,CLICKED)
        
        self.input.bind("menu",KEYBOARD.ESCAPE,CLICKED)

        self.mouse_sprite = Sprite("mouse.png")

        self.multiplayer_button = Button(self, pos=[144,64], sprite="button-multiplayer.png", callback=self.button_multiplayer)
        self.singleplayer_button = Button(self, pos=[144,84], sprite="button-singleplayer.png", callback=self.button_singleplayer)
        self.leave_button = Button(self, pos=[144,104], sprite="button-leave.png", callback=self.button_quit)
        self.title_sprite = Sprite("title.png")
        
        self.gameManager = GameManager(self)
        
        self.island = Island(self)
        self.player = Player(self,True)
        self.player_manager = PlayerManager(self)
        self.network_manager = NetworkManager(self)
        self.player_manager.player_list[None] = self.player
        self.save_manager.set_encryption_key("save0",b"OCqZTMHYWLh1DoCrXUDoI1hU6G9PwS03apyMKMCGBx4=")
        
    def event_quit(self):
        self.running = False

    def begin_transition(self):
        self.transition = True
        
    def button_quit(self):
        if self.network_manager.connected:
            self.network_manager.send_quit()
        self.running = False
        exit(0)
    
    def button_multiplayer(self):
        self.begin_transition()
        self.network_manager.run()
    
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
            self.title_sprite.alpha = self.transition_unit
            
        self.mouse_sprite.alpha = self.transition_unit
              
        if self.input.get("menu"):
            if self.island.catch_book.opened:
                self.island.catch_book.close_book()
            else:
                self.state = "menu"

    def draw(self):
        self.island.draw()

        if self.state == "menu":
            self.window.render(self.title_sprite, [119, 35])
            self.multiplayer_button.draw()
            self.singleplayer_button.draw()
            self.leave_button.draw()
            self.window.render(self.mouse_sprite, self.mouse_pos)
        
        if self.state == "game" and self.island.catch_book.opened:
            self.window.render(self.mouse_sprite, self.mouse_pos)

game = Game()
game.run()