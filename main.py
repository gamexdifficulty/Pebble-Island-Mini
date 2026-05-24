from frostlight_engine import *

class Game(FrostlightEngine):
    def __init__(self):
        super().__init__(canvas_size=[320,180],fps_limit=165)
        self.running = True
        self.state = "game"
    
    def event_quit(self):
        self.running = False
    
    def update(self):
        ...

    def draw(self):
        self.window.fill(200,255,255)

game = Game()
game.run()